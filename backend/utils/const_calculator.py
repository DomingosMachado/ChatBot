def calculate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-4o-mini") -> float:
    # GPT-4o-mini pricing
    input_cost = (input_tokens / 1000) * 0.00015
    output_cost = (output_tokens / 1000) * 0.0006
    return input_cost + output_cost