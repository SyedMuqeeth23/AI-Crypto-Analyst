from openai import OpenAI
from data import get_coin_price, get_top_movers, get_trending_coins, get_major_coins

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def analyze_crypto(question):
    q = question.lower()

    # Decide what data to fetch
    if "gainer" in q or "loser" in q:
        movers = get_top_movers()
        context = f"""
        Top Gainers: {movers['gainers']}
        Top Losers: {movers['losers']}
        """

    elif "trend" in q or "news" in q:
        trending = get_trending_coins()
        context = f"Trending Coins: {trending}"

    elif "doge" in q:
        coin = get_coin_price("dogecoin")
        context = f"DOGE: {coin}"

    elif "bnb" in q:
        coin = get_coin_price("binancecoin")
        context = f"BNB: {coin}"

    elif "eth" in q:
        coin = get_coin_price("ethereum")
        context = f"ETH: {coin}"

    elif "btc" in q or "bitcoin" in q:
        coin = get_coin_price("bitcoin")
        context = f"BTC: {coin}"

    else:
        # Default fallback
        data = get_major_coins()
        context = f"Major Coins: {data}"

    # Prompt
    prompt = f"""
    You are a crypto market research analyst.

    You analyze data and explain insights clearly like a professional.

    Context:
    {context}

    User Question:
    {question}

    Give:
    - Summary
    - Key Insight
    - Market Sentiment (Bullish/Bearish/Neutral)
    """

    response = client.chat.completions.create(
        model="gemma",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content