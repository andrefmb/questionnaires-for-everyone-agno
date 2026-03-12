import os
import json
from agents import gemba_agent, ssa_agent, SSAResponse, GEMBAResponse

def format_input(items, list_type):
    if list_type == 'single':
        return format_list_singles(items)
    elif list_type == 'pairs':
        return format_list_pairs(items)
    else:
        raise AssertionError('List type must be single / pairs.')

def format_list_singles(list):
    formatted = ''
    
    for item in list:
        formatted += item + '\n'

    return formatted

def format_list_pairs(list):
    formatted = ''
    
    for pair in list:
        formatted_pair = pair[0] + ' - ' + pair[1]
        formatted += formatted_pair + '\n'
    
    return formatted

# GEMBA-DA evaluation of translation quality
def evaluate_gemba(source, translation, src_lang, tgt_lang, list_type):
    try:
        # Format input for better comparisons
        src_fmt = format_input(source, list_type)
        tlt_fmt = format_input(translation, list_type)
        
        command = format_gemba_command(src_lang, tgt_lang, src_fmt, tlt_fmt)
        
        response = gemba_agent.run(command)
        
        # Agno agent with output_schema returns a Pydantic model in response.content
        if hasattr(response, 'content') and response.content:
            if isinstance(response.content, GEMBAResponse):
                return {'score': str(response.content.score)}
            elif isinstance(response.content, dict):
                return {'score': str(response.content.get('score', '0'))}
            elif isinstance(response.content, str):
                try:
                    data = json.loads(response.content)
                    return {'score': str(data.get('score', '0'))}
                except json.JSONDecodeError:
                    # Fallback to extract first number if structured output fails
                    import re
                    match = re.search(r'\d+', response.content)
                    return {'score': match.group() if match else "0"}
        
        return {'score': "0"}
    except Exception as e:
        return {'error': str(e)}

# GEMBA GPT instruction formatting
def format_gemba_command(src_lang, tgt_lang, source, target):
    fmt = """Score the following translation from {source_lang} to {target_lang} on a continuous scale from 0 to 100, where a score of zero means \"no meaning preserved\" and score of one hundred means \"perfect meaning and grammar\".
Return the score in the specified JSON format.

{source_lang} source: \"{source_seg}\"
{target_lang} translation: \"{target_seg}\"
""".format(source_lang = src_lang, target_lang = tgt_lang, source_seg = source, target_seg = target)

    return fmt

# SSA (Semantic similarity assessment)
def evaluate_ssa(source, translation, src_lang, tgt_lang, list_type):
    try:
        src_fmt = format_input(source, list_type)
        tlt_fmt = format_input(translation, list_type)
        
        command = format_ssa_command(src_lang, tgt_lang, src_fmt, tlt_fmt)
        
        response = ssa_agent.run(command)
        
        # Agno agent with output_schema returns a Pydantic model in response.content
        if hasattr(response, 'content') and response.content:
            if isinstance(response.content, SSAResponse):
                return response.content.model_dump()
            elif isinstance(response.content, dict):
                return response.content
            elif isinstance(response.content, str):
                try:
                    return json.loads(response.content)
                except json.JSONDecodeError:
                    return {'error': 'Failed to parse agent response as JSON', 'content': response.content}
            return response.content
        
        return {'error': 'No response from agent'}
    except Exception as e:
        return {'error': str(e)}
    
# SSA GPT instruction formatting
def format_ssa_command(src_lang, tgt_lang, source, target):
    fmt = """Assess the semantic similarity of the following texts in {source_lang} and {target_lang} on a scale from 0 (no semantic similarity at all) to 100 (perfect semantic similarity). Justify the score. Provide a single paragraph suggesting changes to the {target_lang} version (i.e. word or expression replacements) to improve the score.
Respond in the specified JSON format.

{source_lang}:  \"{source_text}\"
{target_lang}: \"{target_text}\"
""".format(source_lang = src_lang, target_lang = tgt_lang, source_text = source, target_text = target)
    return fmt