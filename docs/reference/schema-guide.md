# Schema Guide

How to define inputs and outputs for agents.

## Basic Structure

```markdown
## Input
- field: type              # Required
- field: type?             # Optional
- field: type = default    # With default value

## Output
- field: type
- field: ::SharedType::    # Reference a shared type
```

## Types

### Basic Types
- `str` - Text
- `int` - Whole number
- `float` - Decimal
- `bool` - True/false
- `datetime` - Timestamp
- `list[type]` - List of items
- `object` - Nested structure

### Constraints
- `min_length: 10` - Minimum text length
- `max_length: 500` - Maximum text length  
- `min: 0` - Minimum number
- `max: 100` - Maximum number
- `range: [0.0, 1.0]` - Number range

### Options
```markdown
- status: "active" | "pending" | "done"
- depth: "quick" | "standard" | "deep" = "standard"
```


That's all you need to know.