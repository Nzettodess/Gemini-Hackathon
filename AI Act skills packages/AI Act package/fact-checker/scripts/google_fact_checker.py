#!/usr/bin/env python3

import sys
import requests
import os

def fact_check(claim):
    """Simple fact checker - raw string in, raw string out"""
    
    api_key = os.getenv('GOOGLE_FACT_CHECK_API_KEY')
    if not api_key:
        return "ERROR: API key not found"
    # api_key=""
    
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        'query': claim,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return "ERROR: API request failed"
        
        data = response.json()
        claims = data.get('claims', [])
        
        if not claims:
            return "NO_RESULTS"
        
        # Get top 5 results
        top_claims = claims[:5]
        results = []
        
        for i, claim in enumerate(top_claims, 1):
            claim_review = claim.get('claimReview', [{}])[0]
            
            # Combine all claimReview info into summary text (info only, no rating/checker)
            summary_parts = []
            
            # Add title if available
            title = claim_review.get('title', '')
            if title:
                summary_parts.append(title)
            
            # Add review body/text if available
            review_body = claim_review.get('reviewBody', '')
            if review_body:
                summary_parts.append(review_body)
            
            # Add original claim text
            original_claim = claim.get('text', '')
            if original_claim:
                summary_parts.append(f"Original claim: {original_claim}")
            
            # Combine all parts or use fallback
            if summary_parts:
                info_text = " | ".join(summary_parts)
            else:
                info_text = "No detailed content available"
            
            results.append(f"#{i}: {info_text}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python google_fact_checker.py 'claim text'")
        sys.exit(1)
    
    claim = sys.argv[1]
    result = fact_check(claim)
    print(result)
