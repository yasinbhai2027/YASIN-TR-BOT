import asyncio
from pyquotex.stable_api import Quotex
from app import start_server

async def main():
    # ফ্লাস্ক ওয়েব সার্ভিস চালু রাখা
    start_server()
    
    # কোটেক্স একাউন্ট কানেকশন সেটআপ
    client = Quotex(
        email="your_quotex_email@gmail.com", 
        password="your_quotex_password",
        lang="en",
        host="qxbroker.com"
    )
    
    print("📡 Connecting to Quotex WebSocket Live Server...")
    check, reason = await client.connect()
    
    if check:
        print("✅ SUCCESS: Connected to Quotex Direct Live Data Stream!")
        
        payouts = await client.get_all_payout()
        print(f"📊 Current Live Payout Rates: {payouts}")
        
        # ওটিসি বা লাইভ এসেটের রিয়েল-টাইম ক্যান্ডেল সাবস্ক্রাইব
        asset = "EURUSD_otc"
        await client.subscribe_candles(asset, 60)
        
        while True:
            live_candles = client.get_realtime_candles(asset)
            print(f"🕯️ Real-Time Candle Data: {live_candles}")
            await asyncio.sleep(1)
            
    else:
        print("❌ Connection Failed:", reason)

if __name__ == "__main__":
    asyncio.run(main())
