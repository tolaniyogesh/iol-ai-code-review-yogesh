import pytest
import tempfile
import os
from src.config import load_review_config, ReviewConfig


class TestConfig:
    def test_load_default_config(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
version: "1.0"
enabled: true
ignore_patterns:
  - "*.md"
  - "tests/**"
focus_areas:
  code_quality: true
  security: true
""")
            f.flush()
            config_path = f.name
        
        try:
            config = load_review_config(config_path)
            
            assert config.version == "1.0"
            assert config.enabled is True
            assert "*.md" in config.ignore_patterns
            assert config.focus_areas.code_quality is True
            assert config.focus_areas.security is True
        finally:
            os.unlink(config_path)
    
    def test_load_nonexistent_config(self):
        config = load_review_config("nonexistent.yaml")
        
        assert isinstance(config, ReviewConfig)
        assert config.enabled is True
    
    def test_custom_rules_parsing(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
version: "1.0"
custom_rules:
  - name: "Test Rule"
    pattern: "test_pattern"
    severity: "critical"
    message: "Test message"
""")
            f.flush()
            config_path = f.name
        
        try:
            config = load_review_config(config_path)
            
            assert len(config.custom_rules) == 1
            assert config.custom_rules[0].name == "Test Rule"
            assert config.custom_rules[0].severity == "critical"
        finally:
            os.unlink(config_path)
