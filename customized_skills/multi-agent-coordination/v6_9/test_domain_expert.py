"""
Test Suite for Domain Expert System v4.0

Tests all components:
- KnowledgeBase
- RuleEngine
- InferenceEngine
- DomainExpert
"""

import sys
from datetime import datetime

from domain_expert import (
    DomainExpert,
    KnowledgeBase,
    RuleEngine,
    InferenceEngine,
    Fact,
    Rule,
    Concept,
    InferenceResult,
    FactType,
    RuleType,
    InferenceMethod,
    create_domain_expert,
    create_chess_expert,
    create_coding_expert,
)


def test_knowledge_base():
    """Test KnowledgeBase"""
    print("Testing KnowledgeBase...")
    
    kb = KnowledgeBase()
    
    # Test add_fact
    fact1 = Fact(
        id="fact1",
        statement="The sky is blue",
        fact_type=FactType.ATOMIC,
        confidence=0.95,
    )
    kb.add_fact(fact1)
    assert len(kb.facts) == 1, "Should have 1 fact"
    
    # Test get_fact
    retrieved = kb.get_fact("fact1")
    assert retrieved == fact1, "Should retrieve fact"
    
    # Test find_facts
    results = kb.find_facts("sky")
    assert len(results) == 1, "Should find fact"
    
    # Test add_concept
    concept1 = Concept(
        id="concept1",
        name="Sky",
        definition="The atmosphere above Earth",
        synonyms=["heavens", "firmament"],
    )
    kb.add_concept(concept1)
    assert len(kb.concepts) == 1, "Should have 1 concept"
    
    # Test find_concept
    found = kb.find_concept("Sky")
    assert found == concept1, "Should find concept"
    
    # Test find by synonym
    found = kb.find_concept("heavens")
    assert found == concept1, "Should find by synonym"
    
    # Test get_statistics
    stats = kb.get_statistics()
    assert stats["total_facts"] == 1, "Should have 1 fact"
    assert stats["total_concepts"] == 1, "Should have 1 concept"
    
    print("  [OK] KnowledgeBase tests passed")
    return True


def test_rule_engine():
    """Test RuleEngine"""
    print("Testing RuleEngine...")
    
    engine = RuleEngine()
    
    # Test add_rule
    rule1 = Rule(
        id="rule1",
        name="Test Rule",
        description="A test rule",
        rule_type=RuleType.DEDUCTIVE,
        premises=["sky is blue"],
        conclusions=["it is daytime"],
        priority=5,
    )
    engine.add_rule(rule1)
    assert len(engine.rules) == 1, "Should have 1 rule"
    
    # Test get_rule
    retrieved = engine.get_rule("rule1")
    assert retrieved == rule1, "Should retrieve rule"
    
    # Test find_applicable_rules
    applicable = engine.find_applicable_rules(["sky is blue"])
    assert len(applicable) == 1, "Should find applicable rule"
    assert applicable[0].id == "rule1", "Should be rule1"
    
    # Test explain_rule
    explanation = engine.explain_rule("rule1")
    assert "sky is blue" in explanation, "Should explain premises"
    assert "it is daytime" in explanation, "Should explain conclusions"
    
    print("  [OK] RuleEngine tests passed")
    return True


def test_inference_engine():
    """Test InferenceEngine"""
    print("Testing InferenceEngine...")
    
    kb = KnowledgeBase()
    engine = RuleEngine()
    inference = InferenceEngine(kb, engine)
    
    # Add rules
    rule1 = Rule(
        id="rule1",
        name="Socrates Rule",
        description="All men are mortal",
        rule_type=RuleType.DEDUCTIVE,
        premises=["socrates is a man"],
        conclusions=["socrates is mortal"],
        confidence=1.0,
    )
    engine.add_rule(rule1)
    
    # Test forward chaining
    result = inference.forward_chain(["socrates is a man"])
    assert result.success, "Should succeed"
    assert len(result.conclusions) == 1, "Should infer 1 fact"
    assert result.conclusions[0].statement == "socrates is mortal", "Should infer mortality"
    
    # Test backward chaining
    result = inference.backward_chain(
        "socrates is mortal",
        ["socrates is a man"]
    )
    assert result.success, "Should succeed"
    assert len(result.conclusions) == 1, "Should prove 1 fact"
    
    # Test bidirectional inference
    result = inference.infer(
        "socrates is mortal",
        ["socrates is a man"],
        InferenceMethod.BIDIRECTIONAL
    )
    assert result.success, "Should succeed"
    
    print("  [OK] InferenceEngine tests passed")
    return True


def test_domain_expert():
    """Test DomainExpert"""
    print("Testing DomainExpert...")
    
    expert = DomainExpert("test_domain")
    
    # Test add_concept FIRST (before adding facts that might match)
    concept = Concept(
        id="concept1",
        name="Python",
        definition="A programming language",
    )
    expert.add_concept(concept)
    assert len(expert.knowledge_base.concepts) == 1, "Should have 1 concept"
    
    # Test ask with concept
    result = expert.ask("Python")
    assert result["answer_type"] == "concept", f"Should find concept, got {result['answer_type']}"
    
    # Test add_knowledge
    fact = Fact(
        id="fact1",
        statement="Python is a programming language",
        fact_type=FactType.ATOMIC,
    )
    expert.add_knowledge(fact)
    assert len(expert.knowledge_base.facts) == 1, "Should have 1 fact"
    
    # Test add_rule
    rule = Rule(
        id="rule1",
        name="Python Rule",
        description="Python is interpreted",
        rule_type=RuleType.DEDUCTIVE,
        premises=["language is Python"],
        conclusions=["language is interpreted"],
    )
    expert.add_rule(rule)
    assert len(expert.rule_engine.rules) == 1, "Should have 1 rule"
    
    # Test ask with direct fact
    fact2 = Fact(
        id="fact2",
        statement="Java is also a language",
        fact_type=FactType.ATOMIC,
    )
    expert.add_knowledge(fact2)
    
    result = expert.ask("Java")
    assert result["answer_type"] == "direct", "Should find direct fact"
    
    # Test get_expertise_summary
    summary = expert.get_expertise_summary()
    assert summary["domain"] == "test_domain", "Should have domain name"
    assert summary["facts"] == 2, "Should have 2 facts"
    assert summary["concepts"] == 1, "Should have 1 concept"
    assert summary["rules"] == 1, "Should have 1 rule"
    
    print("  [OK] DomainExpert tests passed")
    return True


def test_chess_expert():
    """Test chess expert creation"""
    print("Testing Chess Expert...")
    
    expert = create_chess_expert()
    
    # Check domain
    assert expert.domain_name == "chinese_chess", "Should be chess domain"
    
    # Check concepts
    general = expert.knowledge_base.find_concept("将")
    assert general is not None, "Should find general concept"
    assert "king" in general.synonyms, "Should have synonym"
    
    # Check rules
    assert len(expert.rule_engine.rules) >= 2, "Should have chess rules"
    
    # Test ask
    result = expert.ask("general")
    assert result["answer_type"] == "concept", "Should find general"
    
    print("  [OK] Chess Expert tests passed")
    return True


def test_coding_expert():
    """Test coding expert creation"""
    print("Testing Coding Expert...")
    
    expert = create_coding_expert()
    
    # Check domain
    assert expert.domain_name == "software_engineering", "Should be coding domain"
    
    # Check concepts
    refactoring = expert.knowledge_base.find_concept("refactoring")
    assert refactoring is not None, "Should find refactoring"
    
    # Check rules
    assert len(expert.rule_engine.rules) >= 2, "Should have coding rules"
    
    # Test ask
    result = expert.ask("refactoring")
    assert result["answer_type"] == "concept", "Should find refactoring"
    
    print("  [OK] Coding Expert tests passed")
    return True


def test_data_serialization():
    """Test data class serialization"""
    print("Testing data serialization...")
    
    # Test Fact serialization
    fact = Fact(
        id="test",
        statement="Test fact",
        fact_type=FactType.ATOMIC,
        confidence=0.9,
    )
    data = fact.to_dict()
    restored = Fact.from_dict(data)
    assert restored.id == fact.id, "Should restore ID"
    assert restored.statement == fact.statement, "Should restore statement"
    
    # Test Rule serialization
    rule = Rule(
        id="test",
        name="Test Rule",
        description="A test",
        rule_type=RuleType.DEDUCTIVE,
        premises=["A"],
        conclusions=["B"],
    )
    data = rule.to_dict()
    restored = Rule.from_dict(data)
    assert restored.name == rule.name, "Should restore name"
    assert restored.premises == rule.premises, "Should restore premises"
    
    # Test Concept serialization
    concept = Concept(
        id="test",
        name="Test",
        definition="A test concept",
        synonyms=["test1", "test2"],
    )
    data = concept.to_dict()
    restored = Concept.from_dict(data)
    assert restored.name == concept.name, "Should restore name"
    assert restored.synonyms == concept.synonyms, "Should restore synonyms"
    
    print("  [OK] Data serialization tests passed")
    return True


def test_complex_inference():
    """Test complex inference scenarios"""
    print("Testing complex inference...")
    
    kb = KnowledgeBase()
    engine = RuleEngine()
    inference = InferenceEngine(kb, engine)
    
    # Create chain of rules
    # A -> B -> C -> D
    rule1 = Rule(
        id="r1",
        name="A to B",
        description="If A then B",
        rule_type=RuleType.DEDUCTIVE,
        premises=["A is true"],
        conclusions=["B is true"],
        confidence=0.9,
    )
    rule2 = Rule(
        id="r2",
        name="B to C",
        description="If B then C",
        rule_type=RuleType.DEDUCTIVE,
        premises=["B is true"],
        conclusions=["C is true"],
        confidence=0.8,
    )
    rule3 = Rule(
        id="r3",
        name="C to D",
        description="If C then D",
        rule_type=RuleType.DEDUCTIVE,
        premises=["C is true"],
        conclusions=["D is true"],
        confidence=0.95,
    )
    
    engine.add_rule(rule1)
    engine.add_rule(rule2)
    engine.add_rule(rule3)
    
    # Forward chain from A
    result = inference.forward_chain(["A is true"])
    assert result.success, "Should succeed"
    assert len(result.conclusions) == 3, "Should infer B, C, D"
    
    # Check confidence propagation
    # min(0.9, 0.8, 0.95) = 0.8
    assert result.confidence == 0.8, f"Should have confidence 0.8, got {result.confidence}"
    
    print("  [OK] Complex inference tests passed")
    return True


def test_exceptions():
    """Test rule exceptions"""
    print("Testing rule exceptions...")
    
    kb = KnowledgeBase()
    engine = RuleEngine()
    inference = InferenceEngine(kb, engine)
    
    # Rule with exception - use exact matching for simplicity
    rule = Rule(
        id="r1",
        name="Bird Rule",
        description="Birds can fly",
        rule_type=RuleType.DEFEASIBLE,
        premises=["tweety is a bird"],
        conclusions=["tweety can fly"],
        exceptions=["tweety is a penguin", "tweety is an ostrich"],
    )
    engine.add_rule(rule)
    
    # Should fire without exception
    result = inference.forward_chain(["tweety is a bird"])
    assert result.success, f"Should succeed, got: {result}"
    assert len(result.conclusions) == 1, "Should infer flight"
    
    # Should not fire with exception
    result = inference.forward_chain(["tweety is a bird", "tweety is a penguin"])
    assert not result.success, "Should not fire due to exception"
    
    print("  [OK] Exception tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Domain Expert System v4.0 - Test Suite")
    print("=" * 60)
    
    tests = [
        test_knowledge_base,
        test_rule_engine,
        test_inference_engine,
        test_domain_expert,
        test_chess_expert,
        test_coding_expert,
        test_data_serialization,
        test_complex_inference,
        test_exceptions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            print(f"  [FAILED] {test.__name__}: {e}")
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
