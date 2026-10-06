import urllib.request
import urllib.parse
import json
import glob
import os

files = glob.glob('test_files/*.txt')
print(f"Found {len(files)} test files.\n")

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc_type = 'essay'
    if 'resume' in fname:
        doc_type = 'resume'
    elif 'paper' in fname:
        doc_type = 'research'
    elif 'sop' in fname:
        doc_type = 'cover_letter'

    data = urllib.parse.urlencode({'text': content, 'document_type': doc_type}).encode()
    req = urllib.request.Request('http://127.0.0.1:8000/analyze-text', data=data)
    
    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read())
        print(f"=== {fname} ({result['document_type_name']}) ===")
        print(f"Overall AI Score : {result['overall_ai_probability']}%")
        print(f"Verdict          : {result['verdict']} (Color: {result['verdict_color']})")
        print(f"Word Count       : {result['document_stats']['word_count']} words")
        print(f"Sentence Count   : {result['document_stats']['sentence_count']} sentences")
        print(f"AI Sentences     : {result['document_stats']['ai_sentences']}")
        print(f"Human Sentences  : {result['document_stats']['human_sentences']}")
        print(f"Flesch-Kincaid   : {result['readability']['flesch_kincaid_grade']} Grade Level")
        print(f"Perplexity Score : {result['metrics']['perplexity_score']}%")
        print(f"Burstiness Score : {result['metrics']['burstiness_score']}%")
        print(f"Vocabulary Score : {result['metrics']['vocabulary_score']}%")
        print("-" * 50)
    except Exception as e:
        print(f"Error analyzing {fname}: {e}")
