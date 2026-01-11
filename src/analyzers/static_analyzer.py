import re
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.models import ReviewComment, Severity
from src.logger import setup_logger

logger = setup_logger(__name__)


class StaticAnalyzer:
    def __init__(self):
        self.security_patterns = [
            (r'(password|pwd|passwd)\s*=\s*["\'][^"\']+["\']', 
             "Hardcoded password detected", Severity.CRITICAL),
            (r'(api_key|apikey|api-key)\s*=\s*["\'][^"\']+["\']',
             "Hardcoded API key detected", Severity.CRITICAL),
            (r'(secret|token)\s*=\s*["\'][^"\']+["\']',
             "Hardcoded secret detected", Severity.CRITICAL),
            (r'eval\s*\(',
             "Use of eval() is dangerous and should be avoided", Severity.WARNING),
            (r'exec\s*\(',
             "Use of exec() is dangerous and should be avoided", Severity.WARNING),
            (r'__import__\s*\(',
             "Dynamic imports can be security risks", Severity.WARNING),
        ]
        
        self.code_quality_patterns = [
            (r'print\s*\(',
             "Use logging instead of print statements", Severity.SUGGESTION),
            (r'TODO:|FIXME:|HACK:',
             "TODO/FIXME comment found - consider addressing", Severity.SUGGESTION),
            (r'^\s*pass\s*$',
             "Empty pass statement - consider implementing or removing", Severity.SUGGESTION),
        ]
    
    def analyze_file(self, file_path: str, content: str, 
                    custom_rules: List[Dict[str, Any]] = None) -> List[ReviewComment]:
        comments = []
        
        comments.extend(self._check_patterns(file_path, content, self.security_patterns, "Security"))
        comments.extend(self._check_patterns(file_path, content, self.code_quality_patterns, "Code Quality"))
        
        if custom_rules:
            custom_patterns = [
                (rule['pattern'], rule['message'], self._parse_severity(rule['severity']))
                for rule in custom_rules
            ]
            comments.extend(self._check_patterns(file_path, content, custom_patterns, "Custom Rule"))
        
        if file_path.endswith('.py'):
            comments.extend(self._analyze_python_specific(file_path, content))
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            comments.extend(self._analyze_javascript_specific(file_path, content))
        
        return comments
    
    def _check_patterns(self, file_path: str, content: str, 
                       patterns: List[tuple], category: str) -> List[ReviewComment]:
        comments = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern, message, severity in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    comments.append(ReviewComment(
                        file_path=file_path,
                        line_number=line_num,
                        severity=severity,
                        category=category,
                        message=message,
                        code_snippet=line.strip()
                    ))
        
        return comments
    
    def _analyze_python_specific(self, file_path: str, content: str) -> List[ReviewComment]:
        comments = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('def ') and '"""' not in content[content.find(stripped):content.find(stripped) + 200]:
                if not any(lines[i].strip().startswith('"""') or lines[i].strip().startswith("'''") 
                          for i in range(max(0, line_num), min(len(lines), line_num + 3))):
                    comments.append(ReviewComment(
                        file_path=file_path,
                        line_number=line_num,
                        severity=Severity.SUGGESTION,
                        category="Documentation",
                        message="Function missing docstring",
                        suggestion="Add a docstring describing the function's purpose, parameters, and return value"
                    ))
            
            if 'except:' in stripped or 'except :' in stripped:
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity=Severity.WARNING,
                    category="Best Practices",
                    message="Bare except clause catches all exceptions",
                    suggestion="Specify the exception type(s) to catch"
                ))
            
            if re.search(r'==\s*True|==\s*False', stripped):
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity=Severity.SUGGESTION,
                    category="Code Quality",
                    message="Unnecessary comparison with True/False",
                    suggestion="Use 'if variable:' or 'if not variable:' instead"
                ))
        
        return comments
    
    def _analyze_javascript_specific(self, file_path: str, content: str) -> List[ReviewComment]:
        comments = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if re.search(r'\bvar\s+', stripped):
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity=Severity.SUGGESTION,
                    category="Best Practices",
                    message="Use 'const' or 'let' instead of 'var'",
                    suggestion="Replace 'var' with 'const' for constants or 'let' for variables"
                ))
            
            if '==' in stripped and '===' not in stripped:
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity=Severity.SUGGESTION,
                    category="Best Practices",
                    message="Use strict equality (===) instead of loose equality (==)",
                    suggestion="Replace '==' with '==='"
                ))
            
            if 'console.log' in stripped:
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity=Severity.SUGGESTION,
                    category="Code Quality",
                    message="Remove console.log statement before production",
                    suggestion="Use a proper logging library or remove debug statements"
                ))
        
        return comments
    
    def _parse_severity(self, severity: str) -> Severity:
        severity_map = {
            'critical': Severity.CRITICAL,
            'warning': Severity.WARNING,
            'suggestion': Severity.SUGGESTION
        }
        return severity_map.get(severity.lower(), Severity.SUGGESTION)
