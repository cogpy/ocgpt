"""
MOSES-like Program Representation Implementation (v1)

Based on cards/moses/program-representation.md and schemas/program.json
"""

import random
import math
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class ExprKind(Enum):
    CONST = "const"
    VAR = "var"
    OP = "op"


class DataType(Enum):
    BOOL = "Bool"
    REAL = "Real"
    INT = "Int"
    SYMBOL = "Symbol"


@dataclass
class Expression:
    """Expression node in program tree"""
    kind: ExprKind
    value: Any = None
    name: str = None
    op: str = None
    args: List['Expression'] = None
    data_type: DataType = DataType.REAL
    
    def __post_init__(self):
        if self.args is None:
            self.args = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to JSON-compatible dict following schema"""
        result = {"kind": self.kind.value}
        
        if self.value is not None:
            result["value"] = self.value
        if self.name:
            result["name"] = self.name
        if self.op:
            result["op"] = self.op
        if self.args:
            result["args"] = [arg.to_dict() for arg in self.args]
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expression':
        """Create expression from dict"""
        kind = ExprKind(data["kind"])
        args = [cls.from_dict(arg_data) for arg_data in data.get("args", [])]
        
        return cls(
            kind=kind,
            value=data.get("value"),
            name=data.get("name"),
            op=data.get("op"),
            args=args
        )
    
    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluate expression given variable assignments"""
        if self.kind == ExprKind.CONST:
            return self.value
        elif self.kind == ExprKind.VAR:
            return variables.get(self.name, 0)
        elif self.kind == ExprKind.OP:
            return self._evaluate_operation(variables)
        else:
            raise ValueError(f"Unknown expression kind: {self.kind}")
    
    def _evaluate_operation(self, variables: Dict[str, Any]) -> Any:
        """Evaluate operation with given arguments"""
        arg_values = [arg.evaluate(variables) for arg in self.args]
        
        # Arithmetic operators
        if self.op == "+":
            return sum(arg_values)
        elif self.op == "-":
            if len(arg_values) == 1:
                return -arg_values[0]
            return arg_values[0] - sum(arg_values[1:])
        elif self.op == "*":
            result = 1
            for val in arg_values:
                result *= val
            return result
        elif self.op == "/":
            if len(arg_values) != 2:
                raise ValueError("Division requires exactly 2 arguments")
            denominator = arg_values[1]
            if abs(denominator) < 1e-10:  # Safe division
                return 0 if arg_values[0] >= 0 else float('-inf')
            return arg_values[0] / denominator
        
        # Comparison operators
        elif self.op == "<":
            return arg_values[0] < arg_values[1]
        elif self.op == "<=":
            return arg_values[0] <= arg_values[1]
        elif self.op == "=":
            return arg_values[0] == arg_values[1]
        elif self.op == ">=":
            return arg_values[0] >= arg_values[1]
        elif self.op == ">":
            return arg_values[0] > arg_values[1]
        
        # Logical operators
        elif self.op == "and":
            return all(arg_values)
        elif self.op == "or":
            return any(arg_values)
        elif self.op == "not":
            if len(arg_values) != 1:
                raise ValueError("Not requires exactly 1 argument")
            return not arg_values[0]
        
        # Conditional
        elif self.op == "if":
            if len(arg_values) != 3:
                raise ValueError("If requires exactly 3 arguments: condition, then, else")
            condition, then_val, else_val = arg_values
            return then_val if condition else else_val
        
        # Aggregates
        elif self.op == "mean":
            return sum(arg_values) / len(arg_values) if arg_values else 0
        elif self.op == "sum":
            return sum(arg_values)
        
        else:
            raise ValueError(f"Unknown operation: {self.op}")
    
    def __str__(self):
        if self.kind == ExprKind.CONST:
            return str(self.value)
        elif self.kind == ExprKind.VAR:
            return self.name
        elif self.kind == ExprKind.OP:
            if len(self.args) == 1:
                return f"{self.op}({self.args[0]})"
            elif len(self.args) == 2:
                return f"({self.args[0]} {self.op} {self.args[1]})"
            else:
                args_str = ", ".join(str(arg) for arg in self.args)
                return f"{self.op}({args_str})"
        return f"Expression({self.kind})"


class Program:
    """Program following schemas/program.json"""
    
    def __init__(self, expression: Expression, id: str = None, meta: Dict[str, Any] = None):
        self.id = id or f"p:program_{random.randint(1000, 9999)}"
        self.expression = expression
        self.meta = meta or {}
        self.fitness = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to JSON-compatible dict"""
        return {
            "id": self.id,
            "type": "Program",
            "out": self.expression.to_dict(),
            "meta": self.meta
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        """Create program from dict"""
        expression = Expression.from_dict(data["out"])
        return cls(
            expression=expression,
            id=data["id"],
            meta=data.get("meta", {})
        )
    
    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluate program with given variable assignments"""
        return self.expression.evaluate(variables)
    
    def __str__(self):
        return f"Program({self.id}): {self.expression}"


class ProgramGenerator:
    """Generate random programs for MOSES-like evolution"""
    
    def __init__(self, 
                 variables: List[str],
                 max_depth: int = 4,
                 operators: List[str] = None):
        self.variables = variables
        self.max_depth = max_depth
        self.operators = operators or ["+", "-", "*", "/", "<", ">", "=", "and", "or", "not", "if"]
        
        # Probabilities for generation
        self.const_prob = 0.3
        self.var_prob = 0.3
        self.op_prob = 0.4
    
    def generate_expression(self, depth: int = 0) -> Expression:
        """Generate random expression tree"""
        if depth >= self.max_depth:
            # Force terminal (const or var)
            if random.random() < 0.5:
                return self.generate_constant()
            else:
                return self.generate_variable()
        
        # Choose expression type
        rand = random.random()
        if rand < self.const_prob:
            return self.generate_constant()
        elif rand < self.const_prob + self.var_prob:
            return self.generate_variable()
        else:
            return self.generate_operation(depth)
    
    def generate_constant(self) -> Expression:
        """Generate constant expression"""
        value = random.choice([
            random.randint(-10, 10),  # integers
            random.uniform(-5, 5),    # floats
            random.choice([True, False])  # booleans
        ])
        
        return Expression(
            kind=ExprKind.CONST,
            value=value
        )
    
    def generate_variable(self) -> Expression:
        """Generate variable expression"""
        name = random.choice(self.variables)
        return Expression(
            kind=ExprKind.VAR,
            name=name
        )
    
    def generate_operation(self, depth: int) -> Expression:
        """Generate operation expression"""
        op = random.choice(self.operators)
        
        # Determine number of arguments based on operation
        if op in ["not"]:
            num_args = 1
        elif op in ["if"]:
            num_args = 3
        elif op in ["mean", "sum"]:
            num_args = random.randint(2, 4)
        else:
            num_args = 2
        
        args = []
        for _ in range(num_args):
            args.append(self.generate_expression(depth + 1))
        
        return Expression(
            kind=ExprKind.OP,
            op=op,
            args=args
        )
    
    def generate_program(self) -> Program:
        """Generate random program"""
        expression = self.generate_expression()
        return Program(expression)


class MOSESEvolver:
    """Simple MOSES-like evolutionary algorithm"""
    
    def __init__(self, 
                 variables: List[str],
                 fitness_function: Callable[[Program, List[Dict[str, Any]]], float],
                 population_size: int = 50,
                 generations: int = 100,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7):
        
        self.variables = variables
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        self.generator = ProgramGenerator(variables)
        self.population = []
        self.best_programs = []
    
    def evolve(self, training_data: List[Dict[str, Any]], target_key: str) -> List[Program]:
        """
        Evolve population to fit training data
        
        Args:
            training_data: List of dicts with variable assignments and target values
            target_key: Key in training_data dicts containing target output
        """
        # Initialize population
        self.population = []
        for _ in range(self.population_size):
            program = self.generator.generate_program()
            self.population.append(program)
        
        # Evolution loop
        for generation in range(self.generations):
            # Evaluate fitness
            for program in self.population:
                program.fitness = self.fitness_function(program, training_data, target_key)
            
            # Sort by fitness (higher is better)
            self.population.sort(key=lambda p: p.fitness, reverse=True)
            
            # Keep track of best programs
            if not self.best_programs or self.population[0].fitness > self.best_programs[0].fitness:
                self.best_programs = self.population[:5].copy()  # Top 5
            
            # Selection and reproduction
            new_population = []
            
            # Keep top performers (elitism)
            elite_size = max(1, self.population_size // 10)
            new_population.extend(self.population[:elite_size])
            
            # Generate rest of population
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection()
                
                if random.random() < self.crossover_rate:
                    parent2 = self.tournament_selection()
                    child = self.crossover(parent1, parent2)
                else:
                    child = self.copy_program(parent1)
                
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)
                
                new_population.append(child)
            
            self.population = new_population
        
        # Final evaluation
        for program in self.population:
            program.fitness = self.fitness_function(program, training_data, target_key)
        
        self.population.sort(key=lambda p: p.fitness, reverse=True)
        return self.population[:10]  # Return top 10
    
    def tournament_selection(self, tournament_size: int = 3) -> Program:
        """Select parent using tournament selection"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda p: p.fitness)
    
    def crossover(self, parent1: Program, parent2: Program) -> Program:
        """Simple crossover by swapping subtrees"""
        # For simplicity, just randomly choose one parent's expression
        # A more sophisticated version would swap random subtrees
        parent = random.choice([parent1, parent2])
        return self.copy_program(parent)
    
    def mutate(self, program: Program) -> Program:
        """Mutate program by replacing a random node"""
        # Simple mutation: regenerate a random subtree
        new_expr = self.generator.generate_expression(depth=random.randint(0, 2))
        return Program(new_expr)
    
    def copy_program(self, program: Program) -> Program:
        """Create a copy of a program"""
        return Program.from_dict(program.to_dict())


def accuracy_fitness(program: Program, training_data: List[Dict[str, Any]], target_key: str) -> float:
    """Default fitness function based on accuracy"""
    correct = 0
    total = 0
    
    for data_point in training_data:
        try:
            predicted = program.evaluate(data_point)
            actual = data_point[target_key]
            
            # For boolean/classification tasks
            if isinstance(actual, bool):
                if bool(predicted) == actual:
                    correct += 1
            # For regression tasks (with tolerance)
            else:
                error = abs(predicted - actual)
                if error < 0.1:  # tolerance
                    correct += 1
            
            total += 1
        except Exception:
            # Penalize programs that crash
            total += 1
    
    return correct / total if total > 0 else 0.0


def mdl_fitness(program: Program, training_data: List[Dict[str, Any]], target_key: str) -> float:
    """Fitness based on Minimum Description Length principle"""
    accuracy = accuracy_fitness(program, training_data, target_key)
    complexity = count_nodes(program.expression)
    
    # Balance accuracy vs complexity
    mdl_score = accuracy - (complexity * 0.01)  # penalty for complexity
    return max(0.0, mdl_score)


def count_nodes(expression: Expression) -> int:
    """Count number of nodes in expression tree"""
    count = 1
    for arg in expression.args:
        count += count_nodes(arg)
    return count