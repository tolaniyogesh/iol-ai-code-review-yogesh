import pytest
from src.analyzers.static_analyzer import StaticAnalyzer
from src.models import Severity


class TestStaticAnalyzer:
    def setup_method(self):
        self.analyzer = StaticAnalyzer()
    
    def test_detect_hardcoded_password(self):
        code = '''
password = "admin123"
api_key = "sk-1234567890"
'''
        comments = self.analyzer.analyze_file("test.py", code)
        
        assert len(comments) >= 2
        assert any("password" in c.message.lower() for c in comments)
        assert any(c.severity == Severity.CRITICAL for c in comments)
    
    def test_detect_eval_usage(self):
        code = '''
result = eval(user_input)
'''
        comments = self.analyzer.analyze_file("test.py", code)
        
        assert len(comments) > 0
        assert any("eval" in c.message.lower() for c in comments)
    
    def test_detect_print_statements(self):
        code = '''
print("Debug message")
'''
        comments = self.analyzer.analyze_file("test.py", code)
        
        assert len(comments) > 0
        assert any("print" in c.message.lower() for c in comments)
    
    def test_python_bare_except(self):
        code = '''
try:
    something()
except:
    pass
'''
        comments = self.analyzer.analyze_file("test.py", code)
        
        assert len(comments) > 0
        assert any("except" in c.message.lower() for c in comments)
    
    def test_javascript_var_usage(self):
        code = '''
var x = 10;
var name = "test";
'''
        comments = self.analyzer.analyze_file("test.js", code)
        
        assert len(comments) >= 2
        assert any("var" in c.message.lower() for c in comments)
    
    def test_javascript_loose_equality(self):
        code = '''
if (x == 5) {
    console.log("equal");
}
'''
        comments = self.analyzer.analyze_file("test.js", code)
        
        assert len(comments) > 0
        assert any("===" in c.message or "equality" in c.message.lower() for c in comments)
    
    def test_custom_rules(self):
        code = '''
secret_token = "abc123"
'''
        custom_rules = [{
            'pattern': r'secret_token\s*=',
            'message': 'Custom rule: No secret tokens',
            'severity': 'critical'
        }]
        
        comments = self.analyzer.analyze_file("test.py", code, custom_rules)
        
        assert len(comments) > 0
        assert any("Custom rule" in c.message for c in comments)
    
    def test_no_issues_clean_code(self):
        code = '''
import logging

logger = logging.getLogger(__name__)

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b
'''
        comments = self.analyzer.analyze_file("test.py", code)
        
        assert len(comments) == 0
