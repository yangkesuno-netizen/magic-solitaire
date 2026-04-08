"""
Domain Expert System v4.0 - Complete Restoration

Core Components:
- DomainExpert: Expert in a specific domain with knowledge and rules
- KnowledgeBase: Manages domain knowledge (facts, concepts, relationships)
- RuleEngine: Executes rules based on conditions
- InferenceEngine: Performs forward/backward chaining inference

Size: ~14.6KB (complete implementation)
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


# ============================================================================
# Core Data Structures
# ============================================================================

class FactType(Enum):
    """Types of facts in knowledge base"""
    FACT = auto()        # Basic fact (alias for ATOMIC)
    ATOMIC = auto()      # Simple fact: "sky is blue"
    COMPOUND = auto()    # Complex fact with structure
    RELATIONAL = auto()  # Relationship between entities
    TEMPORAL = auto()    # Time-based fact
    UNCERTAIN = auto()   # Fact with confidence level


class RuleType(Enum):
    """Types of rules"""
    DEDUCTIVE = auto()   # If A then B
    INDUCTIVE = auto()   # A observed, likely B
    ABDUCTIVE = auto()   # B true, maybe A
    DEFEASIBLE = auto()  # Default rule with exceptions


class InferenceMethod(Enum):
    """Inference methods"""
    FORWARD_CHAINING = auto()   # Data-driven
    BACKWARD_CHAINING = auto()  # Goal-driven
    BIDIRECTIONAL = auto()      # Both directions


@dataclass
class Fact:
    """A fact in the knowledge base"""
    id: str
    statement: str
    fact_type: FactType
    confidence: float = 1.0  # 0.0 to 1.0
    source: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "fact_type": self.fact_type.name,
            "confidence": self.confidence,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Fact:
        return cls(
            id=data["id"],
            statement=data["statement"],
            fact_type=FactType[data["fact_type"]],
            confidence=data["confidence"],
            source=data.get("source"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Rule:
    """A rule for inference"""
    id: str
    name: str
    description: str
    rule_type: RuleType
    premises: List[str]  # Conditions that must be true
    conclusions: List[str]  # What can be inferred
    confidence: float = 1.0
    priority: int = 0  # Higher = more important
    exceptions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rule_type": self.rule_type.name,
            "premises": self.premises,
            "conclusions": self.conclusions,
            "confidence": self.confidence,
            "priority": self.priority,
            "exceptions": self.exceptions,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Rule:
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            rule_type=RuleType[data["rule_type"]],
            premises=data["premises"],
            conclusions=data["conclusions"],
            confidence=data["confidence"],
            priority=data["priority"],
            exceptions=data.get("exceptions", []),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Concept:
    """A concept in the domain"""
    id: str
    name: str
    definition: str
    properties: Dict[str, Any] = field(default_factory=dict)
    synonyms: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    parent_concepts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "definition": self.definition,
            "properties": self.properties,
            "synonyms": self.synonyms,
            "related_concepts": self.related_concepts,
            "parent_concepts": self.parent_concepts,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Concept:
        return cls(
            id=data["id"],
            name=data["name"],
            definition=data["definition"],
            properties=data.get("properties", {}),
            synonyms=data.get("synonyms", []),
            related_concepts=data.get("related_concepts", []),
            parent_concepts=data.get("parent_concepts", []),
        )


@dataclass
class InferenceResult:
    """Result of an inference operation"""
    success: bool
    conclusions: List[Fact]
    rules_fired: List[str]
    steps: int
    confidence: float
    explanation: List[str] = field(default_factory=list)


# ============================================================================
# Knowledge Base
# ============================================================================

class KnowledgeBase:
    """Manages domain knowledge"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.facts: Dict[str, Fact] = {}
        self.concepts: Dict[str, Concept] = {}
        self.fact_index: Dict[str, Set[str]] = defaultdict(set)  # statement -> fact_ids
        self.concept_index: Dict[str, Set[str]] = defaultdict(set)  # name -> concept_ids
        
        self.storage_path = Path(storage_path) if storage_path else None
        if self.storage_path and self.storage_path.exists():
            self._load_from_disk()
    
    def add_fact(
        self,
        fact: Union[Fact, str],
        statement: Optional[str] = None,
        fact_type: FactType = FactType.ATOMIC,
        confidence: float = 1.0
    ) -> Fact:
        """Add a fact to the knowledge base
        
        Supports two calling styles:
        1. add_fact(Fact(...)) - Pass a Fact object
        2. add_fact("id", "statement", FactType.FACT) - Pass individual fields
        
        Returns:
            The added Fact object
        """
        if isinstance(fact, Fact):
            # Style 1: Fact object passed
            fact_obj = fact
        else:
            # Style 2: Individual fields
            fact_obj = Fact(
                id=fact,
                statement=statement or fact,
                fact_type=fact_type,
                confidence=confidence,
            )
        
        self.facts[fact_obj.id] = fact_obj
        self.fact_index[fact_obj.statement.lower()].add(fact_obj.id)
        
        if self.storage_path:
            self._save_to_disk()
        
        return fact_obj
    
    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """Get a fact by ID"""
        return self.facts.get(fact_id)
    
    def find_facts(self, statement_pattern: str) -> List[Fact]:
        """Find facts matching a pattern"""
        pattern = statement_pattern.lower()
        results = []
        
        for stmt, fact_ids in self.fact_index.items():
            if pattern in stmt or re.search(pattern, stmt):
                for fact_id in fact_ids:
                    fact = self.facts.get(fact_id)
                    if fact:
                        results.append(fact)
        
        return results
    
    def add_concept(self, concept: Concept) -> None:
        """Add a concept to the knowledge base"""
        self.concepts[concept.id] = concept
        self.concept_index[concept.name.lower()].add(concept.id)
        
        for synonym in concept.synonyms:
            self.concept_index[synonym.lower()].add(concept.id)
        
        if self.storage_path:
            self._save_to_disk()
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get a concept by ID"""
        return self.concepts.get(concept_id)
    
    def find_concept(self, name: str) -> Optional[Concept]:
        """Find a concept by name or synonym"""
        name_lower = name.lower()
        if name_lower in self.concept_index:
            concept_id = next(iter(self.concept_index[name_lower]))
            return self.concepts.get(concept_id)
        return None
    
    def get_related_concepts(self, concept_id: str) -> List[Concept]:
        """Get concepts related to a given concept"""
        concept = self.concepts.get(concept_id)
        if not concept:
            return []
        
        related = []
        for related_id in concept.related_concepts:
            if related_id in self.concepts:
                related.append(self.concepts[related_id])
        
        return related
    
    def get_concept_hierarchy(self, concept_id: str) -> Dict[str, Any]:
        """Get concept hierarchy (parents and children)"""
        concept = self.concepts.get(concept_id)
        if not concept:
            return {}
        
        return {
            "concept": concept,
            "parents": [self.concepts.get(pid) for pid in concept.parent_concepts if pid in self.concepts],
            "children": [c for c in self.concepts.values() if concept_id in c.parent_concepts],
        }
    
    def query(self, query_str: str) -> Dict[str, List[Any]]:
        """Query the knowledge base"""
        results = {
            "facts": self.find_facts(query_str),
            "concepts": [],
        }
        
        # Check if query matches a concept
        concept = self.find_concept(query_str)
        if concept:
            results["concepts"].append(concept)
        
        return results
    
    def get_statistics(self) -> Dict[str, int]:
        """Get knowledge base statistics"""
        return {
            "total_facts": len(self.facts),
            "total_concepts": len(self.concepts),
            "fact_types": len(set(f.fact_type for f in self.facts.values())),
        }
    
    def _save_to_disk(self) -> None:
        """Save knowledge base to disk"""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "facts": {k: v.to_dict() for k, v in self.facts.items()},
            "concepts": {k: v.to_dict() for k, v in self.concepts.items()},
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def _load_from_disk(self) -> None:
        """Load knowledge base from disk"""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        try:
            data = json.loads(self.storage_path.read_text())
            for fact_id, fact_data in data.get("facts", {}).items():
                self.add_fact(Fact.from_dict(fact_data))
            for concept_id, concept_data in data.get("concepts", {}).items():
                self.add_concept(Concept.from_dict(concept_data))
        except Exception:
            pass


# ============================================================================
# Rule Engine
# ============================================================================

class RuleEngine:
    """Executes rules based on conditions"""
    
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.rule_index: Dict[str, Set[str]] = defaultdict(set)  # premise -> rule_ids
    
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the engine"""
        self.rules[rule.id] = rule
        
        # Index by premises
        for premise in rule.premises:
            self.rule_index[premise.lower()].add(rule.id)
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID"""
        return self.rules.get(rule_id)
    
    def find_applicable_rules(self, known_facts: List[str]) -> List[Rule]:
        """Find rules that can be applied given known facts"""
        applicable = []
        known_set = set(f.lower() for f in known_facts)
        
        for rule in self.rules.values():
            # Check if all premises are satisfied
            if all(premise.lower() in known_set for premise in rule.premises):
                # Check exceptions
                if not any(exc.lower() in known_set for exc in rule.exceptions):
                    applicable.append(rule)
        
        # Sort by priority
        applicable.sort(key=lambda r: r.priority, reverse=True)
        return applicable
    
    def fire_rule(self, rule: Rule, known_facts: Dict[str, Fact]) -> List[Fact]:
        """Fire a rule and generate conclusions"""
        conclusions = []
        
        for conclusion_stmt in rule.conclusions:
            fact = Fact(
                id=f"inferred_{rule.id}_{hash(conclusion_stmt) % 10000}",
                statement=conclusion_stmt,
                fact_type=FactType.INFERRED if hasattr(FactType, 'INFERRED') else FactType.COMPOUND,
                confidence=rule.confidence,
                source=f"rule:{rule.id}",
                metadata={"inferred_from": rule.id},
            )
            conclusions.append(fact)
        
        return conclusions
    
    def get_rules_by_type(self, rule_type: RuleType) -> List[Rule]:
        """Get all rules of a specific type"""
        return [r for r in self.rules.values() if r.rule_type == rule_type]
    
    def explain_rule(self, rule_id: str) -> Optional[str]:
        """Generate human-readable explanation of a rule"""
        rule = self.rules.get(rule_id)
        if not rule:
            return None
        
        premises = " AND ".join(rule.premises)
        conclusions = " THEN ".join(rule.conclusions)
        return f"IF {premises} THEN {conclusions}"


# ============================================================================
# Inference Engine
# ============================================================================

class InferenceEngine:
    """Performs forward and backward chaining inference"""
    
    def __init__(self, knowledge_base: KnowledgeBase, rule_engine: RuleEngine):
        self.kb = knowledge_base
        self.rule_engine = rule_engine
        self.max_iterations = 100
    
    def forward_chain(
        self,
        initial_facts: List[str],
        goal: Optional[str] = None
    ) -> InferenceResult:
        """Forward chaining: from facts to conclusions"""
        known_facts = set(f.lower() for f in initial_facts)
        inferred_facts: List[Fact] = []
        rules_fired: List[str] = []
        explanation: List[str] = []
        
        iteration = 0
        new_facts_added = True
        
        while new_facts_added and iteration < self.max_iterations:
            new_facts_added = False
            iteration += 1
            
            # Find applicable rules
            applicable = self.rule_engine.find_applicable_rules(list(known_facts))
            
            for rule in applicable:
                if rule.id in rules_fired:
                    continue
                
                # Fire the rule
                conclusions = self.rule_engine.fire_rule(rule, {})
                
                for fact in conclusions:
                    fact_key = fact.statement.lower()
                    if fact_key not in known_facts:
                        known_facts.add(fact_key)
                        inferred_facts.append(fact)
                        self.kb.add_fact(fact)
                        new_facts_added = True
                        
                        explanation.append(
                            f"Fired rule '{rule.name}': {self.rule_engine.explain_rule(rule.id)}"
                        )
                        
                        # Check if goal reached
                        if goal and goal.lower() == fact_key:
                            return InferenceResult(
                                success=True,
                                conclusions=inferred_facts,
                                rules_fired=rules_fired,
                                steps=iteration,
                                confidence=fact.confidence,
                                explanation=explanation,
                            )
                
                rules_fired.append(rule.id)
        
        return InferenceResult(
            success=len(inferred_facts) > 0,
            conclusions=inferred_facts,
            rules_fired=rules_fired,
            steps=iteration,
            confidence=min(f.confidence for f in inferred_facts) if inferred_facts else 0.0,
            explanation=explanation,
        )
    
    def backward_chain(
        self,
        goal: str,
        known_facts: List[str]
    ) -> InferenceResult:
        """Backward chaining: from goal to supporting facts"""
        known_set = set(f.lower() for f in known_facts)
        goals_to_prove = [goal.lower()]
        proven_facts: List[Fact] = []
        rules_fired: List[str] = []
        explanation: List[str] = []
        
        iteration = 0
        
        while goals_to_prove and iteration < self.max_iterations:
            iteration += 1
            current_goal = goals_to_prove.pop(0)
            
            # Check if already known
            if current_goal in known_set:
                continue
            
            # Find rules that conclude this goal
            supporting_rules = []
            for rule in self.rule_engine.rules.values():
                if any(current_goal == conc.lower() for conc in rule.conclusions):
                    supporting_rules.append(rule)
            
            if not supporting_rules:
                # Cannot prove this goal
                return InferenceResult(
                    success=False,
                    conclusions=proven_facts,
                    rules_fired=rules_fired,
                    steps=iteration,
                    confidence=0.0,
                    explanation=explanation + [f"Cannot prove: {current_goal}"],
                )
            
            # Try to prove premises of the first supporting rule
            rule = supporting_rules[0]
            can_fire = True
            
            for premise in rule.premises:
                premise_key = premise.lower()
                if premise_key not in known_set:
                    goals_to_prove.append(premise_key)
                    can_fire = False
            
            if can_fire:
                # Fire the rule
                conclusions = self.rule_engine.fire_rule(rule, {})
                for fact in conclusions:
                    if fact.statement.lower() == current_goal:
                        proven_facts.append(fact)
                        known_set.add(current_goal)
                        rules_fired.append(rule.id)
                        explanation.append(
                            f"Proved '{current_goal}' using rule '{rule.name}'"
                        )
                        break
        
        return InferenceResult(
            success=len(proven_facts) > 0,
            conclusions=proven_facts,
            rules_fired=rules_fired,
            steps=iteration,
            confidence=min(f.confidence for f in proven_facts) if proven_facts else 0.0,
            explanation=explanation,
        )
    
    def infer(
        self,
        query: str,
        known_facts: Optional[List[str]] = None,
        method: InferenceMethod = InferenceMethod.BIDIRECTIONAL
    ) -> InferenceResult:
        """General inference method"""
        known = known_facts or []
        
        if method == InferenceMethod.FORWARD_CHAINING:
            return self.forward_chain(known, query)
        elif method == InferenceMethod.BACKWARD_CHAINING:
            return self.backward_chain(query, known)
        else:  # BIDIRECTIONAL
            # Try forward first
            result = self.forward_chain(known, query)
            if result.success:
                return result
            
            # Try backward
            return self.backward_chain(query, known)


# ============================================================================
# Domain Expert
# ============================================================================

class DomainExpert:
    """Expert system for a specific domain"""
    
    def __init__(self, domain_name: str, storage_path: Optional[str] = None):
        self.domain_name = domain_name
        self.knowledge_base = KnowledgeBase(storage_path)
        self.rule_engine = RuleEngine()
        self.inference_engine = InferenceEngine(self.knowledge_base, self.rule_engine)
    
    def add_knowledge(self, fact: Fact) -> None:
        """Add knowledge to the expert"""
        self.knowledge_base.add_fact(fact)
    
    def add_concept(self, concept: Concept) -> None:
        """Add a concept to the expert"""
        self.knowledge_base.add_concept(concept)
    
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the expert"""
        self.rule_engine.add_rule(rule)
    
    def ask(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ask the expert a question"""
        # First, try to find direct facts
        facts = self.knowledge_base.find_facts(question)
        
        if facts:
            return {
                "answer_type": "direct",
                "facts": [f.to_dict() for f in facts],
                "confidence": max(f.confidence for f in facts),
            }
        
        # Try inference
        known_facts = context.get("known_facts", []) if context else []
        result = self.inference_engine.infer(question, known_facts)
        
        if result.success:
            return {
                "answer_type": "inferred",
                "facts": [f.to_dict() for f in result.conclusions],
                "confidence": result.confidence,
                "explanation": result.explanation,
                "steps": result.steps,
            }
        
        # Try to find related concepts
        concept = self.knowledge_base.find_concept(question)
        if concept:
            return {
                "answer_type": "concept",
                "concept": concept.to_dict(),
                "related": [c.to_dict() for c in self.knowledge_base.get_related_concepts(concept.id)],
            }
        
        return {
            "answer_type": "unknown",
            "message": f"I don't have knowledge about '{question}' in {self.domain_name}",
        }
    
    def explain(self, fact_id: str) -> Optional[str]:
        """Explain how a fact was derived"""
        fact = self.knowledge_base.get_fact(fact_id)
        if not fact:
            return None
        
        if fact.source and fact.source.startswith("rule:"):
            rule_id = fact.source.split(":")[1]
            return self.rule_engine.explain_rule(rule_id)
        
        return f"Fact '{fact.statement}' was directly asserted."
    
    def get_expertise_summary(self) -> Dict[str, Any]:
        """Get summary of expert's knowledge"""
        kb_stats = self.knowledge_base.get_statistics()
        
        return {
            "domain": self.domain_name,
            "facts": kb_stats["total_facts"],
            "concepts": kb_stats["total_concepts"],
            "rules": len(self.rule_engine.rules),
            "rule_types": len(set(r.rule_type for r in self.rule_engine.rules.values())),
        }
    
    def validate_knowledge(self) -> List[Dict[str, Any]]:
        """Validate knowledge base for consistency"""
        issues = []
        
        # Check for circular rules
        for rule_id, rule in self.rule_engine.rules.items():
            for premise in rule.premises:
                for other_rule in self.rule_engine.rules.values():
                    if other_rule.id != rule_id:
                        if any(premise.lower() == conc.lower() for conc in other_rule.conclusions):
                            if any(p.lower() == rule.conclusions[0].lower() for p in other_rule.premises):
                                issues.append({
                                    "type": "circular_rule",
                                    "rule": rule_id,
                                    "message": f"Potential circular dependency with rule {other_rule.id}",
                                })
        
        # Check for orphaned concepts
        for concept_id, concept in self.knowledge_base.concepts.items():
            for parent_id in concept.parent_concepts:
                if parent_id not in self.knowledge_base.concepts:
                    issues.append({
                        "type": "orphaned_concept",
                        "concept": concept_id,
                        "message": f"Parent concept '{parent_id}' not found",
                    })
        
        return issues


# ============================================================================
# Domain Expert Factory
# ============================================================================

def create_domain_expert(domain_name: str, storage_path: Optional[str] = None) -> DomainExpert:
    """Factory function to create a domain expert"""
    return DomainExpert(domain_name, storage_path)


def create_chess_expert() -> DomainExpert:
    """Create a chess domain expert"""
    expert = DomainExpert("chinese_chess")
    
    # Add chess concepts
    expert.add_concept(Concept(
        id="general",
        name="将/帅",
        definition="The most important piece in Chinese chess",
        properties={"value": 10000, "movement": "palace_only"},
        synonyms=["king", "general", "jiang", "shuai"],
    ))
    
    expert.add_concept(Concept(
        id="chariot",
        name="车",
        definition="Most powerful piece, moves horizontally and vertically",
        properties={"value": 900, "movement": "rook_like"},
        synonyms=["rook", "chariot", "ju", "che"],
    ))
    
    # Add chess rules
    expert.add_rule(Rule(
        id="general_check",
        name="General in Check",
        description="When general is under attack, must respond",
        rule_type=RuleType.DEDUCTIVE,
        premises=["general is under attack"],
        conclusions=["must move general or block attack"],
        priority=10,
    ))
    
    expert.add_rule(Rule(
        id="capture_value",
        name="Capture High Value",
        description="Capturing high value pieces is generally good",
        rule_type=RuleType.DEFEASIBLE,
        premises=["can capture opponent piece", "piece value > 100"],
        conclusions=["should consider capturing"],
        exceptions=["capture exposes general"],
        priority=5,
    ))
    
    return expert


def create_coding_expert() -> DomainExpert:
    """Create a coding domain expert"""
    expert = DomainExpert("software_engineering")
    
    # Add coding concepts
    expert.add_concept(Concept(
        id="refactoring",
        name="Refactoring",
        definition="Improving code structure without changing behavior",
        properties={"category": "maintenance"},
        synonyms=["code cleanup", "restructuring"],
    ))
    
    expert.add_concept(Concept(
        id="unit_test",
        name="Unit Test",
        definition="Testing individual units of code in isolation",
        properties={"category": "testing"},
        synonyms=["unit testing", "test case"],
    ))
    
    # Add coding rules
    expert.add_rule(Rule(
        id="test_coverage",
        name="Test Coverage",
        description="Code should have adequate test coverage",
        rule_type=RuleType.DEFEASIBLE,
        premises=["code is production ready"],
        conclusions=["should have >80% test coverage"],
        exceptions=["code is prototype", "code is generated"],
    ))
    
    expert.add_rule(Rule(
        id="code_review",
        name="Code Review",
        description="All code should be reviewed before merging",
        rule_type=RuleType.DEDUCTIVE,
        premises=["code change is significant"],
        conclusions=["requires code review"],
        priority=8,
    ))
    
    return expert


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "DomainExpert",
    "KnowledgeBase",
    "RuleEngine",
    "InferenceEngine",
    "Fact",
    "Rule",
    "Concept",
    "InferenceResult",
    "FactType",
    "RuleType",
    "InferenceMethod",
    "create_domain_expert",
    "create_chess_expert",
    "create_coding_expert",
]
