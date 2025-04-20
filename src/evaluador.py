import nltk
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Descargar recursos de nltk si no están
nltk.download('punkt')

def evaluar_respuestas(respuestasCSV, respuestasLLM):


    

    # Inicializar métricas
    bleu_scores = []
    rouge_l_scores = []
    bertscore_precisions = []
    bertscore_recalls = []
    bertscore_fscores = []

    tokenizer = nltk.word_tokenize
    smoother = SmoothingFunction().method4
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

    # Para BERTScore
    P, R, F1 = bert_score(respuestasCSV, respuestasLLM, lang="es", rescale_with_baseline=True)

    for i, (ref, pred) in enumerate(zip(respuestasCSV, respuestasLLM)):
        # BLEU
        ref_tokens = tokenizer(ref)
        pred_tokens = tokenizer(pred)
        bleu = sentence_bleu([ref_tokens], pred_tokens, smoothing_function=smoother)
        bleu_scores.append(bleu)

        # ROUGE-L
        rouge = scorer.score(ref, pred)['rougeL'].fmeasure
        rouge_l_scores.append(rouge)

        # BERTScore
        bertscore_precisions.append(P[i].item())
        bertscore_recalls.append(R[i].item())
        bertscore_fscores.append(F1[i].item())

    # Promedios
    #print("\n=== MÉTRICAS PROMEDIO ===")
    #print(f"BLEU:         {sum(bleu_scores)/len(bleu_scores):.4f}")
    #print(f"ROUGE-L:      {sum(rouge_l_scores)/len(rouge_l_scores):.4f}")
    #print(f"BERTScore F1: {sum(bertscore_fscores)/len(bertscore_fscores):.4f}")

    return {
        "BLEU": sum(bleu_scores)/len(bleu_scores),
        "ROUGE-L": sum(rouge_l_scores)/len(rouge_l_scores),
        "BERTScore F1": sum(bertscore_fscores)/len(bertscore_fscores)
    }
