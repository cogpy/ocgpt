## cards/moses/program-representation.md **Title:** MOSES-like Program Representation **Version:** 0.1 ### Representation * Programs are typed expression trees. * **Node kinds:** const, var, op (n-ary). * **Types:** Bool, Real, Int, Symbol. ### Operators (starter set) * Arithmetic: + - * / (safe division w/ ε) * Comparators: < ≤ = ≥ > * Logical: and or not * Conditional: if(cond, a, b) * Aggregates: mean(list), sum(list) *(optional)* ### Example
json
{
  "id": "p:rule1",
  "type": "Program",
  "out": {
    "kind": "op",
    "op": "and",
    "args": [
      {"kind": "op", "op": ">", "args": [{"kind":"var","name":"x"},{"kind":"const","value":3}]},
      {"kind": "op", "op": "not", "args": [{"kind":"var","name":"rain"}]}
    ]
  }
}
### Fitness (abstract) * Defined per task, e.g., accuracy, MDL, or agreement with PLN-derived beliefs. * Use cross-validation; report top-k programs with fitness and a brief rationale.