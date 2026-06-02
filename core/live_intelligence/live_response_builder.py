"""
Live Response Builder

Builds LLM prompts that include live intelligence context
and instructions for safe, source-aware responses.
"""

from typing import Dict, List


def build_live_prompt(user_input: str, context: Dict) -> str:
    """
    Build an LLM prompt that includes live intelligence context.
    
    Args:
        user_input: The original user question
        context: The live intelligence context from get_live_news_context()
        
    Returns:
        A formatted prompt string for the LLM
    """
    
    confidence = context.get("confidence", "low")
    results = context.get("results", [])
    validation = context.get("validation", {})
    
    # Build the context block
    context_lines = _build_context_block(results, validation, confidence)
    
    # Build instructions based on confidence
    instructions = _build_instructions(confidence, validation)
    
    # Assemble the complete prompt
    prompt = f"""You are JARVIS, Janon's private AI assistant.

USER'S QUESTION:
{user_input}

LIVE INTELLIGENCE CONTEXT:
{context_lines}

INSTRUCTIONS FOR ANSWERING:
{instructions}

IMPORTANT:
- Answer ONLY based on the live context provided above.
- Do NOT make up facts or hallucinate information.
- Always cite your sources and include domain names.
- If information conflicts between sources, mention the discrepancy.
- Be transparent about confidence level: "{confidence.upper()}".
{_confidence_specific_instructions(confidence)}

Provide a clear, factual answer based only on the live context above:
"""
    
    return prompt.strip()


def _build_context_block(
    results: List[Dict],
    validation: Dict,
    confidence: str
) -> str:
    """
    Build the context block showing search results and validation.
    
    Args:
        results: Search results
        validation: Validation results
        confidence: Confidence level
        
    Returns:
        Formatted context block
    """
    
    lines = []
    
    # Check for errors first
    for result in results:
        if result.get("type") == "error":
            return f"ERROR: {result.get('message', 'Search failed')}\n\nFallback: Answer based on your training data, but note this information may not be current."
    
    # Add validation summary
    lines.append("VALIDATION SUMMARY:")
    validation_notes = validation.get("validation_notes", "No validation data")
    lines.append(f"  {validation_notes}")
    
    # Add trusted sources count
    trusted = validation.get("trusted_sources", 0)
    domains = validation.get("unique_domains", 0)
    lines.append(f"  Trusted sources: {trusted}/{domains}")
    
    # Add AI summary if available
    lines.append("\nAI GENERATED SUMMARY:")
    summary_found = False
    for result in results:
        if result.get("type") == "answer":
            lines.append(f"  {result.get('content', 'No summary available')}")
            summary_found = True
            break
    if not summary_found:
        lines.append("  No AI summary available")
    
    # Add individual sources
    lines.append("\nSOURCES:")
    non_error_results = [r for r in results if r.get("type") not in ("error", "answer")]
    
    if not non_error_results:
        lines.append("  No sources found")
    else:
        for i, result in enumerate(non_error_results, 1):
            source = result.get("source", "Unknown")
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")
            published = result.get("published_date", "")
            
            lines.append(f"\n  [{i}] {source}")
            if title:
                lines.append(f"      Title: {title}")
            if published:
                lines.append(f"      Date: {published}")
            if content:
                # Truncate long content
                truncated = content[:250] + "..." if len(content) > 250 else content
                lines.append(f"      Content: {truncated}")
            if url:
                lines.append(f"      URL: {url}")
    
    return "\n".join(lines)


def _build_instructions(confidence: str, validation: Dict) -> str:
    """
    Build confidence-specific instructions for the LLM.
    
    Args:
        confidence: Confidence level (low/medium/high)
        validation: Validation results
        
    Returns:
        Formatted instructions
    """
    
    lines = []
    
    if confidence == "high":
        lines.append("CONFIDENCE IS HIGH - You can provide a direct answer.")
        lines.append("- The information comes from multiple trusted, independent sources.")
        lines.append("- Mention the primary sources.")
    
    elif confidence == "medium":
        lines.append("CONFIDENCE IS MEDIUM - Provide a careful answer.")
        lines.append("- The information comes from some trusted sources, but may be limited.")
        lines.append("- Acknowledge the limitations and mention what sources agree.")
        lines.append("- Suggest verifying on official sources if important.")
    
    else:  # low
        lines.append("CONFIDENCE IS LOW - Be very cautious.")
        lines.append("- The information may be incomplete or from less-established sources.")
        lines.append("- Clearly state the limitations and caveats.")
        lines.append("- Do NOT claim certainty about anything.")
        lines.append("- Recommend official sources for verification.")
        lines.append("- Do NOT fill gaps with knowledge cutoff information.")
    
    # Add recommendations
    recommendations = validation.get("recommendations", [])
    if recommendations:
        lines.append("\nRECOMMENDATIONS:")
        for rec in recommendations:
            lines.append(f"- {rec}")
    
    return "\n".join(lines)


def _confidence_specific_instructions(confidence: str) -> str:
    """
    Get additional instructions based on confidence level.
    
    Args:
        confidence: Confidence level
        
    Returns:
        Additional instructions
    """
    
    if confidence == "high":
        return """- You can be fairly confident in the accuracy of this information.
- Cite specific sources by name."""
    
    elif confidence == "medium":
        return """- Acknowledge that some aspects may need verification.
- Use phrases like "according to sources", "reports indicate", "multiple sources suggest"."""
    
    else:  # low
        return """- Use cautious language: "Reportedly", "some sources suggest", "unconfirmed reports indicate"
- Do NOT answer as if you have current knowledge.
- Do NOT claim this is definitely true.
- Suggest the user check official sources for critical decisions."""
