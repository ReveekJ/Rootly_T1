import re
import json
from datetime import datetime, timedelta, timezone


class LogsParser:
    ISO_TIMESTAMP = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?')
    LOG_LEVELS = re.compile(r'\b(ERROR|WARN|WARNING|INFO|DEBUG|TRACE)\b', re.IGNORECASE)

    def __init__(self, line: str):
        self.__text = line

    def extract_timestamp(self, text):
        match = self.ISO_TIMESTAMP.search(text)
        if match:
            ts_str = match.group(0)
            # Replace trailing Z with +00:00 to make it ISO-compliant for fromisoformat
            if ts_str.endswith('Z'):
                ts_str = ts_str[:-1] + '+00:00'
            try:
                ts = datetime.fromisoformat(ts_str)
                # ensure timezone-aware (UTC) if no tzinfo present
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                return ts
            except ValueError:
                return None
        return None

    def extract_log_level(self, text):
        match = self.LOG_LEVELS.search(text)
        return match.group(0).upper() if match else 'INFO'

    def parse_json_safe(self, value):
        # Accept a JSON string or a python object; return parsed dict or original value
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # try to return raw string if it's not JSON
                return value
        return value

    def determine_section(self, text):
        # Example heuristic: look for known section tags in the text
        # Adjust rules as needed for your log format.
        lowered = text.lower()
        if 'auth' in lowered or 'login' in lowered:
            return 'auth'
        if 'db' in lowered or 'database' in lowered:
            return 'database'
        if 'http' in lowered or 'request' in lowered or 'response' in lowered:
            return 'http'
        return 'general'

    def parse_log_entry(self, line, previous_ts=None):
        # Ensure previous_ts is timezone-aware UTC if provided
        if previous_ts is not None and previous_ts.tzinfo is None:
            previous_ts = previous_ts.replace(tzinfo=timezone.utc)

        try:
            obj = json.loads(line)
            # timestamp: check @timestamp then fallback to extraction or previous_ts + 1s
            ts_val = obj.get('@timestamp')
            ts = None
            if ts_val:
                if isinstance(ts_val, str):
                    ts = self.extract_timestamp(ts_val) or None
                    # try direct fromisoformat if not matched by regex
                    if ts is None:
                        try:
                            t = datetime.fromisoformat(ts_val.replace('Z', '+00:00'))
                            ts = t if t.tzinfo else t.replace(tzinfo=timezone.utc)
                        except Exception:
                            ts = None
                elif isinstance(ts_val, (int, float)):
                    # assume epoch seconds
                    ts = datetime.fromtimestamp(ts_val, tz=timezone.utc)
            if ts is None:
                ts = self.extract_timestamp(line)
            if ts is None:
                if previous_ts is not None:
                    ts = previous_ts + timedelta(seconds=1)
                else:
                    ts = datetime.now(timezone.utc)

            level = obj.get('@level') or self.extract_log_level(line)
            section = obj.get('section') or self.determine_section(line)
            tf_req_id = obj.get('tf_req_id')
            req_body = self.parse_json_safe(obj.get('tf_http_req_body'))
            res_body = self.parse_json_safe(obj.get('tf_http_res_body'))
            return {
                'timestamp': ts,
                'level': level,
                'section': section,
                'tf_req_id': tf_req_id,
                'request_body': req_body,
                'response_body': res_body,
                'raw': line,
            }
        except json.JSONDecodeError:
            # fallback parse from text with regex heuristics
            ts = self.extract_timestamp(line)
            if ts is None:
                if previous_ts is not None:
                    ts = previous_ts + timedelta(seconds=1)
                else:
                    ts = datetime.now(timezone.utc)
            level = self.extract_log_level(line)
            section = self.determine_section(line)
            return {'timestamp': ts, 'level': level, 'raw': line, 'section': section}
