import json
import re
from datetime import datetime, timedelta


class LogsParser:
    ISO_TIMESTAMP = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?')
    LOG_LEVELS = re.compile(r'\b(ERROR|WARN|WARNING|INFO|DEBUG|TRACE)\b', re.IGNORECASE)

    def log_debug(self, message):
        print(f"[DEBUG {datetime.utcnow().isoformat()}] {message}")

    def extract_timestamp(self, text):
        match = self.ISO_TIMESTAMP.search(text)
        if match:
            ts = datetime.fromisoformat(match.group(0).replace('Z', '+00:00'))
            self.log_debug(f"Timestamp extracted: {ts}")
            return ts
        self.log_debug("Timestamp not found, returning None")
        return None

    def extract_log_level(self, text):
        match = self.LOG_LEVELS.search(text)
        if match:
            level = match.group(0).upper()
            self.log_debug(f"Log level found: {level}")
            return level
        self.log_debug("Log level not found, defaulting to INFO")
        return 'INFO'

    def parse_section_type(self, text):
        if re.search(r'terraform\s+plan', text, re.IGNORECASE):
            self.log_debug("Section 'plan' detected")
            return 'plan'
        elif re.search(r'terraform\s+apply', text, re.IGNORECASE):
            self.log_debug("Section 'apply' detected")
            return 'apply'
        return None

    def safe_json_parse(self, json_text):
        try:
            if json_text and json_text.strip() != "":
                parsed = json.loads(json_text)
                self.log_debug("JSON body parsed successfully")
                return parsed
            else:
                self.log_debug("JSON body is empty or whitespace")
                return None
        except Exception as e:
            self.log_debug(f"Failed to parse JSON body: {e}")
            return None

    def ensure_body_info(self, body, body_name):
        if body is None or (isinstance(body, str) and body.strip() == ""):
            self.log_debug(f"{body_name} is empty, substituting with placeholder")
            return {"info": f"{body_name} is empty or not provided"}
        return body

    def parse_log_entry(self, line, previous_timestamp=None):
        self.log_debug(f"Parsing line: {line[:80]}...")  # выводим первые 80 символов
        try:
            obj = json.loads(line)
            ts = obj.get('@timestamp') or self.extract_timestamp(line) or (
                previous_timestamp + timedelta(seconds=1) if previous_timestamp else None)
            level = obj.get('@level') or self.extract_log_level(line)
            section = self.parse_section_type(line)
            tf_req_id = obj.get('tf_req_id')
            tf_resource_type = obj.get('tf_resource_type')

            req_body_raw = obj.get('tf_http_req_body')
            res_body_raw = obj.get('tf_http_res_body')
            req_body = self.safe_json_parse(req_body_raw)
            res_body = self.safe_json_parse(res_body_raw)

            # Обеспечиваем наличие информативного тела (если пусто, подставляем placeholder)
            req_body = self.ensure_body_info(req_body, 'request_body')
            res_body = self.ensure_body_info(res_body, 'response_body')

            self.log_debug(f"Parsed JSON entry with tf_req_id={tf_req_id}")

            return {
                'timestamp': ts,
                'level': level,
                'section': section,
                'tf_req_id': tf_req_id,
                'tf_resource_type': tf_resource_type,
                'request_body': req_body,
                'response_body': res_body,
                'raw': line,
            }, ts
        except json.JSONDecodeError:
            ts = self.extract_timestamp(line) or (previous_timestamp + timedelta(seconds=1) if previous_timestamp else None)
            level = self.extract_log_level(line)
            section = self.parse_section_type(line)
            self.log_debug("Parsed as plain text log line")
            return {
                'timestamp': ts,
                'level': level,
                'section': section,
                'raw': line,
                'request_body': {"info": "request_body not available in plain text"},
                'response_body': {"info": "response_body not available in plain text"}
            }, ts

    def parse_log_lines(self, lines):
        parsed_entries = []
        prev_ts = None
        for line in lines:
            entry, prev_ts = self.parse_log_entry(line, prev_ts)
            parsed_entries.append(entry)
        return parsed_entries

