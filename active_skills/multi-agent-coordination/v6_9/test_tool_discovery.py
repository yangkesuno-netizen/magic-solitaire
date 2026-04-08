"""
Test Suite for Tool Discovery System v4.1

High Standard: 100% test pass rate
Tests all components with comprehensive coverage:
- ASTAnalyzer (code analysis, pattern detection)
- ToolRegistry (tool management)
- SecurityValidator (security validation)
- ToolDiscoveryEngine (automatic discovery)
"""

import sys
from datetime import datetime

from tool_discovery import (
    ToolDiscoveryEngine,
    ASTAnalyzer,
    ToolRegistry,
    SecurityValidator,
    Tool,
    DangerousPattern,
    AnalysisResult,
    ValidationResult,
    RiskLevel,
    ToolCategory,
    DANGEROUS_PATTERNS,
    create_tool_discovery_engine,
    analyze_code_security,
    validate_tool_usage,
)


def test_risk_level_enum():
    """Test RiskLevel enum"""
    print("Testing RiskLevel...")
    
    assert RiskLevel.SAFE.name == "SAFE"
    assert RiskLevel.LOW.name == "LOW"
    assert RiskLevel.MEDIUM.name == "MEDIUM"
    assert RiskLevel.HIGH.name == "HIGH"
    assert RiskLevel.CRITICAL.name == "CRITICAL"
    
    print("  [OK] RiskLevel tests passed")
    return True


def test_tool_category_enum():
    """Test ToolCategory enum"""
    print("Testing ToolCategory...")
    
    assert ToolCategory.FILE_IO.name == "FILE_IO"
    assert ToolCategory.NETWORK.name == "NETWORK"
    assert ToolCategory.CODE_EXECUTION.name == "CODE_EXECUTION"
    
    print("  [OK] ToolCategory tests passed")
    return True


def test_dangerous_pattern():
    """Test DangerousPattern data class"""
    print("Testing DangerousPattern...")
    
    pattern = DangerousPattern(
        pattern=r"test\.pattern",
        description="Test pattern",
        risk_level=RiskLevel.MEDIUM,
        category=ToolCategory.FILE_IO,
        mitigation="Use safe alternative",
    )
    
    data = pattern.to_dict()
    assert data["pattern"] == r"test\.pattern"
    assert data["risk_level"] == "MEDIUM"
    assert data["category"] == "FILE_IO"
    
    print("  [OK] DangerousPattern tests passed")
    return True


def test_tool_data_class():
    """Test Tool data class"""
    print("Testing Tool...")
    
    tool = Tool(
        id="test_tool",
        name="Test Tool",
        description="A test tool",
        category=ToolCategory.DATA_PROCESSING,
        risk_level=RiskLevel.LOW,
    )
    
    assert tool.id == "test_tool"
    assert tool.name == "Test Tool"
    assert tool.usage_count == 0
    assert tool.success_rate == 1.0
    
    data = tool.to_dict()
    assert data["id"] == "test_tool"
    assert data["risk_level"] == "LOW"
    
    print("  [OK] Tool tests passed")
    return True


def test_ast_analyzer_creation():
    """Test ASTAnalyzer creation"""
    print("Testing ASTAnalyzer Creation...")
    
    analyzer = ASTAnalyzer()
    assert len(analyzer.patterns) > 0
    
    print("  [OK] ASTAnalyzer creation tests passed")
    return True


def test_ast_analyzer_simple_code():
    """Test ASTAnalyzer with simple code"""
    print("Testing ASTAnalyzer Simple Code...")
    
    analyzer = ASTAnalyzer()
    code = """
import os
import sys

print("Hello")
x = len([1, 2, 3])
"""
    
    result = analyzer.analyze_code(code, "test.py")
    
    assert result.file_path == "test.py"
    assert "os" in result.imports
    assert "sys" in result.imports
    assert "print" in result.functions_called
    assert "len" in result.functions_called
    
    print("  [OK] ASTAnalyzer simple code tests passed")
    return True


def test_ast_analyzer_dangerous_patterns():
    """Test ASTAnalyzer dangerous pattern detection"""
    print("Testing ASTAnalyzer Dangerous Patterns...")
    
    analyzer = ASTAnalyzer()
    # Use simple code without escaped quotes
    code = "result = eval('1 + 1')"
    
    result = analyzer.analyze_code(code, "test.py")
    
    # Should detect code execution pattern (eval/exec)
    pattern_descriptions = [p.description for p in result.patterns_found]
    assert any("code execution" in desc.lower() for desc in pattern_descriptions)
    
    # Risk score should be elevated
    assert result.risk_score > 0
    
    print("  [OK] ASTAnalyzer dangerous patterns tests passed")
    return True


def test_ast_analyzer_risk_score():
    """Test ASTAnalyzer risk score calculation"""
    print("Testing ASTAnalyzer Risk Score...")
    
    analyzer = ASTAnalyzer()
    
    # Safe code
    safe_code = "x = 1 + 2"
    safe_result = analyzer.analyze_code(safe_code)
    assert safe_result.risk_score == 0
    
    # Dangerous code - eval is CRITICAL (50 points)
    dangerous_code = "eval('dangerous_code')"
    dangerous_result = analyzer.analyze_code(dangerous_code)
    assert dangerous_result.risk_score == 50  # CRITICAL = 50 points
    
    print("  [OK] ASTAnalyzer risk score tests passed")
    return True


def test_ast_analyzer_recommendations():
    """Test ASTAnalyzer recommendations"""
    print("Testing ASTAnalyzer Recommendations...")
    
    analyzer = ASTAnalyzer()
    code = "eval('1 + 1')"
    
    result = analyzer.analyze_code(code)
    
    assert len(result.recommendations) > 0
    # Check that recommendations contain eval warning
    assert any("eval" in rec.lower() or "code execution" in rec.lower() 
               for rec in result.recommendations)
    
    print("  [OK] ASTAnalyzer recommendations tests passed")
    return True


def test_tool_registry_creation():
    """Test ToolRegistry creation"""
    print("Testing ToolRegistry Creation...")
    
    registry = ToolRegistry()
    assert len(registry.tools) == 0
    assert len(registry.categories) == len(ToolCategory)
    
    print("  [OK] ToolRegistry creation tests passed")
    return True


def test_tool_registry_register():
    """Test ToolRegistry register"""
    print("Testing ToolRegistry Register...")
    
    registry = ToolRegistry()
    tool = Tool(
        id="test_tool",
        name="Test",
        description="Test tool",
        category=ToolCategory.DATA_PROCESSING,
        risk_level=RiskLevel.LOW,
    )
    
    success = registry.register_tool(tool)
    assert success is True
    assert "test_tool" in registry.tools
    assert "test_tool" in registry.categories[ToolCategory.DATA_PROCESSING]
    
    # Duplicate registration should fail
    success = registry.register_tool(tool)
    assert success is False
    
    print("  [OK] ToolRegistry register tests passed")
    return True


def test_tool_registry_unregister():
    """Test ToolRegistry unregister"""
    print("Testing ToolRegistry Unregister...")
    
    registry = ToolRegistry()
    tool = Tool(
        id="test_tool",
        name="Test",
        description="Test tool",
        category=ToolCategory.DATA_PROCESSING,
        risk_level=RiskLevel.LOW,
    )
    
    registry.register_tool(tool)
    success = registry.unregister_tool("test_tool")
    
    assert success is True
    assert "test_tool" not in registry.tools
    
    # Unregister non-existent should fail
    success = registry.unregister_tool("nonexistent")
    assert success is False
    
    print("  [OK] ToolRegistry unregister tests passed")
    return True


def test_tool_registry_find():
    """Test ToolRegistry find tools"""
    print("Testing ToolRegistry Find...")
    
    registry = ToolRegistry()
    
    # Register tools with different categories
    tool1 = Tool("t1", "Tool 1", "Desc", ToolCategory.FILE_IO, RiskLevel.LOW)
    tool2 = Tool("t2", "Tool 2", "Desc", ToolCategory.NETWORK, RiskLevel.HIGH)
    tool3 = Tool("t3", "Tool 3", "Desc", ToolCategory.FILE_IO, RiskLevel.MEDIUM)
    
    registry.register_tool(tool1)
    registry.register_tool(tool2)
    registry.register_tool(tool3)
    
    # Find by category
    file_tools = registry.get_tools_by_category(ToolCategory.FILE_IO)
    assert len(file_tools) == 2
    
    # Find by risk
    high_risk = registry.get_tools_by_risk(RiskLevel.HIGH)
    assert len(high_risk) == 1
    assert high_risk[0].id == "t2"
    
    # Find with max risk
    safe_tools = registry.find_tools(max_risk=RiskLevel.MEDIUM)
    assert len(safe_tools) == 2
    
    print("  [OK] ToolRegistry find tests passed")
    return True


def test_tool_registry_statistics():
    """Test ToolRegistry statistics"""
    print("Testing ToolRegistry Statistics...")
    
    registry = ToolRegistry()
    tool = Tool("t1", "Tool", "Desc", ToolCategory.DATA_PROCESSING, RiskLevel.LOW)
    registry.register_tool(tool)
    
    stats = registry.get_statistics()
    assert stats["total_tools"] == 1
    assert stats["by_category"]["DATA_PROCESSING"] == 1
    assert stats["by_risk"]["LOW"] == 1
    
    print("  [OK] ToolRegistry statistics tests passed")
    return True


def test_security_validator():
    """Test SecurityValidator"""
    print("Testing SecurityValidator...")
    
    registry = ToolRegistry()
    validator = SecurityValidator(registry)
    
    # Validate non-existent tool
    result = validator.validate_tool("nonexistent")
    assert result.is_valid is False
    assert result.can_execute is False
    
    print("  [OK] SecurityValidator tests passed")
    return True


def test_security_validator_safe_tool():
    """Test SecurityValidator with safe tool"""
    print("Testing SecurityValidator Safe Tool...")
    
    registry = ToolRegistry()
    validator = SecurityValidator(registry)
    
    tool = Tool("safe_tool", "Safe", "Safe tool", ToolCategory.DATA_PROCESSING, RiskLevel.SAFE)
    registry.register_tool(tool)
    
    result = validator.validate_tool("safe_tool")
    
    assert result.is_valid is True
    assert result.can_execute is True
    assert result.risk_level == RiskLevel.SAFE
    assert len(result.warnings) == 0
    
    print("  [OK] SecurityValidator safe tool tests passed")
    return True


def test_security_validator_dangerous_tool():
    """Test SecurityValidator with dangerous tool"""
    print("Testing SecurityValidator Dangerous Tool...")
    
    registry = ToolRegistry()
    validator = SecurityValidator(registry)
    
    tool = Tool("danger_tool", "Danger", "Dangerous tool", ToolCategory.CODE_EXECUTION, RiskLevel.CRITICAL)
    registry.register_tool(tool)
    
    result = validator.validate_tool("danger_tool")
    
    assert result.is_valid is True
    assert result.risk_level == RiskLevel.CRITICAL
    assert len(result.warnings) > 0
    assert "EXECUTE_CRITICAL" in result.required_permissions
    
    print("  [OK] SecurityValidator dangerous tool tests passed")
    return True


def test_security_validator_block():
    """Test SecurityValidator block/unblock"""
    print("Testing SecurityValidator Block...")
    
    registry = ToolRegistry()
    validator = SecurityValidator(registry)
    
    tool = Tool("test_tool", "Test", "Test tool", ToolCategory.DATA_PROCESSING, RiskLevel.LOW)
    registry.register_tool(tool)
    
    # Block tool
    validator.block_tool("test_tool")
    assert validator.is_blocked("test_tool") is True
    
    result = validator.validate_tool("test_tool")
    assert result.is_valid is False
    assert result.can_execute is False
    
    # Unblock tool
    validator.unblock_tool("test_tool")
    assert validator.is_blocked("test_tool") is False
    
    print("  [OK] SecurityValidator block tests passed")
    return True


def test_tool_discovery_engine_creation():
    """Test ToolDiscoveryEngine creation"""
    print("Testing ToolDiscoveryEngine Creation...")
    
    engine = ToolDiscoveryEngine()
    assert engine.registry is not None
    assert engine.analyzer is not None
    assert engine.validator is not None
    
    print("  [OK] ToolDiscoveryEngine creation tests passed")
    return True


def test_tool_discovery_from_code():
    """Test ToolDiscoveryEngine discover from code"""
    print("Testing ToolDiscoveryEngine From Code...")
    
    engine = ToolDiscoveryEngine()
    code = """
import os
import json
print("Hello")
"""
    
    discovered = engine.discover_from_code(code, "test.py")
    
    # Should discover tools from imports
    assert len(discovered) >= 2  # os and json
    
    # Should be registered
    stats = engine.registry.get_statistics()
    assert stats["total_tools"] >= 2
    
    print("  [OK] ToolDiscoveryEngine from code tests passed")
    return True


def test_tool_discovery_builtin_tools():
    """Test ToolDiscoveryEngine builtin tools"""
    print("Testing ToolDiscoveryEngine Builtin Tools...")
    
    engine = ToolDiscoveryEngine()
    builtins = engine.register_builtin_tools()
    
    assert len(builtins) > 0
    
    # Check that print is registered
    tool = engine.registry.get_tool("builtin_print")
    assert tool is not None
    assert tool.name == "print"
    
    print("  [OK] ToolDiscoveryEngine builtin tools tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # Test create_tool_discovery_engine
    engine = create_tool_discovery_engine()
    assert isinstance(engine, ToolDiscoveryEngine)
    
    # Test analyze_code_security
    result = analyze_code_security("x = 1 + 2")
    assert isinstance(result, AnalysisResult)
    assert result.risk_score == 0
    
    # Test validate_tool_usage
    registry = ToolRegistry()
    tool = Tool("test", "Test", "Desc", ToolCategory.DATA_PROCESSING, RiskLevel.LOW)
    registry.register_tool(tool)
    result = validate_tool_usage("test", registry)
    assert isinstance(result, ValidationResult)
    
    print("  [OK] Factory functions tests passed")
    return True


def test_dangerous_patterns_database():
    """Test dangerous patterns database"""
    print("Testing Dangerous Patterns Database...")
    
    # Should have 20+ patterns
    assert len(DANGEROUS_PATTERNS) >= 20
    
    # Check critical patterns exist
    critical = [p for p in DANGEROUS_PATTERNS if p.risk_level == RiskLevel.CRITICAL]
    assert len(critical) >= 2
    
    # Check eval pattern exists
    eval_patterns = [p for p in DANGEROUS_PATTERNS if "eval" in p.pattern]
    assert len(eval_patterns) >= 1
    
    print("  [OK] Dangerous patterns database tests passed")
    return True


def test_analysis_result():
    """Test AnalysisResult data class"""
    print("Testing AnalysisResult...")
    
    result = AnalysisResult(
        file_path="test.py",
        patterns_found=[],
        tools_used=["print", "len"],
        imports=["os"],
        functions_called=["print"],
        risk_score=10,
        recommendations=["Be careful"],
    )
    
    data = result.to_dict()
    assert data["file_path"] == "test.py"
    assert data["risk_score"] == 10
    
    print("  [OK] AnalysisResult tests passed")
    return True


def test_validation_result():
    """Test ValidationResult data class"""
    print("Testing ValidationResult...")
    
    result = ValidationResult(
        tool_id="test",
        is_valid=True,
        risk_level=RiskLevel.LOW,
        warnings=[],
        required_permissions=[],
        can_execute=True,
    )
    
    data = result.to_dict()
    assert data["tool_id"] == "test"
    assert data["is_valid"] is True
    assert data["risk_level"] == "LOW"
    
    print("  [OK] ValidationResult tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Tool Discovery System v4.1 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        test_risk_level_enum,
        test_tool_category_enum,
        test_dangerous_pattern,
        test_tool_data_class,
        test_ast_analyzer_creation,
        test_ast_analyzer_simple_code,
        test_ast_analyzer_dangerous_patterns,
        test_ast_analyzer_risk_score,
        test_ast_analyzer_recommendations,
        test_tool_registry_creation,
        test_tool_registry_register,
        test_tool_registry_unregister,
        test_tool_registry_find,
        test_tool_registry_statistics,
        test_security_validator,
        test_security_validator_safe_tool,
        test_security_validator_dangerous_tool,
        test_security_validator_block,
        test_tool_discovery_engine_creation,
        test_tool_discovery_from_code,
        test_tool_discovery_builtin_tools,
        test_factory_functions,
        test_dangerous_patterns_database,
        test_analysis_result,
        test_validation_result,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  [FAILED] {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  [FAILED] {test.__name__}: {e}")
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed ({passed/len(tests)*100:.1f}%)")
    print("=" * 60)
    
    if failed == 0:
        print("[OK] ALL TESTS PASSED - High Standard Achieved!")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
