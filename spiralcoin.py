#!/usr/bin/env python3
"""
SpiralCoin ∷ Certification of Care

Command-line interface for minting SpiralCoins—
tokens that certify care rendered, not speculate on value.

Usage:
    python spiralcoin.py mint <toneform> <value> <source_description>
    python spiralcoin.py mint-from-transmutation <transmutation_id>
    python spiralcoin.py list
    python spiralcoin.py stats
    python spiralcoin.py template <coin_number>
    python spiralcoin.py verify <coin_number>
    python spiralcoin.py verify-all
"""

import sys
import json
from pathlib import Path
import click
from datetime import datetime

# Add the spiral directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from spiral.spiralcoin import SpiralCoinMinter, SpiralCoinTemplate
from spiral.spiralcoin.coin_core import SpiralCoinLedger
from spiral.spiralcoin.verification import SpiralCoinVerifier


def mint_coin(toneform: str, value: float, source_description: str):
    """Mint a new SpiralCoin."""
    print(f"🪙 Minting SpiralCoin...")
    print(f"   Toneform: {toneform}")
    print(f"   Value: ${value:.2f}")
    print(f"   Source: {source_description}")
    print()
    
    minter = SpiralCoinMinter()
    coin = minter.mint_coin(
        toneform=toneform,
        value=value,
        source_description=source_description
    )
    
    print(f"✅ SpiralCoin {coin.coin_number} minted successfully!")
    print(f"   Coin ID: {coin.coin_id}")
    print(f"   Verification Phrase: \"{coin.verification_phrase}\"")
    print(f"   QR Data: {coin.qr_data}")
    print()
    
    # Generate printable template
    template_gen = SpiralCoinTemplate()
    template_path = template_gen.generate_coin_template(coin)
    print(f"🖨️  Printable template generated: {template_path}")
    
    return coin


def mint_from_transmutation(transmutation_id: str):
    """Mint a SpiralCoin from an existing transmutation."""
    print(f"🪙 Minting SpiralCoin from transmutation {transmutation_id}...")
    
    # Load transmutation data
    transmutations_file = Path("data/transmutations.jsonl")
    if not transmutations_file.exists():
        print("❌ No transmutations found. Please run a transmutation first.")
        return None
    
    transmutation_data = None
    with open(transmutations_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                if data.get('transmutation_id') == transmutation_id:
                    transmutation_data = data
                    break
    
    if not transmutation_data:
        print(f"❌ Transmutation {transmutation_id} not found.")
        return None
    
    minter = SpiralCoinMinter()
    coin = minter.mint_from_transmutation(transmutation_data)
    
    print(f"✅ SpiralCoin {coin.coin_number} minted from transmutation!")
    print(f"   Source: {coin.source_description}")
    print(f"   Value: ${coin.value:.2f}")
    print(f"   Verification Phrase: \"{coin.verification_phrase}\"")
    print()
    
    # Generate printable template
    template_gen = SpiralCoinTemplate()
    template_path = template_gen.generate_coin_template(coin)
    print(f"🖨️  Printable template generated: {template_path}")
    
    return coin


def list_coins():
    """List all minted SpiralCoins."""
    ledger = SpiralCoinLedger()
    coins = ledger.get_all_coins()
    
    if not coins:
        print("🪙 No SpiralCoins have been minted yet.")
        return
    
    print(f"🪙 Found {len(coins)} SpiralCoin(s):")
    print()
    
    for coin in coins:
        print(f"   {coin.coin_number} | ${coin.value:.2f} | {coin.toneform}")
        print(f"      Source: {coin.source_description}")
        print(f"      Minted: {coin.minted_at}")
        print(f"      Phrase: \"{coin.verification_phrase}\"")
        print()


def show_stats():
    """Show SpiralCoin statistics."""
    minter = SpiralCoinMinter()
    stats = minter.get_minting_stats()
    
    print("📊 SpiralCoin Statistics:")
    print()
    print(f"   Total Coins: {stats['total_coins']}")
    print(f"   Total Value: ${stats['total_value':.2f}")
    print()
    
    print("   By Type:")
    for coin_type, count in stats['coins_by_type'].items():
        if count > 0:
            print(f"      {coin_type}: {count}")
    print()
    
    print("   By Status:")
    for status, count in stats['coins_by_status'].items():
        if count > 0:
            print(f"      {status}: {count}")
    print()
    
    if stats['recent_mints']:
        print("   Recent Mints:")
        for mint in stats['recent_mints']:
            print(f"      {mint['coin_number']} | ${mint['value']:.2f} | {mint['source_description']}")


def generate_template(coin_number: str):
    """Generate a printable template for a specific coin."""
    ledger = SpiralCoinLedger()
    coins = ledger.get_all_coins()
    
    target_coin = None
    for coin in coins:
        if coin.coin_number == coin_number:
            target_coin = coin
            break
    
    if not target_coin:
        print(f"❌ SpiralCoin {coin_number} not found.")
        return
    
    print(f"🖨️  Generating template for SpiralCoin {coin_number}...")
    
    template_gen = SpiralCoinTemplate()
    template_path = template_gen.generate_coin_template(target_coin)
    
    print(f"✅ Template generated: {template_path}")
    print(f"   Open this file in a web browser to view and print the SpiralCoin.")


def verify_coin(coin_number: str):
    """Verify a specific SpiralCoin."""
    print(f"🔍 Verifying SpiralCoin {coin_number}...")
    
    verifier = SpiralCoinVerifier()
    result = verifier.verify_coin(coin_number)
    
    if result.get("valid"):
        print(f"✅ SpiralCoin {coin_number} is VALID")
        print(f"   Resonance Score: {result['resonance_score']}%")
        print()
        
        for check_name, check_result in result['checks'].items():
            status = "✅" if check_result['passed'] else "❌"
            print(f"   {status} {check_name.replace('_', ' ').title()}")
            print(f"      {check_result['message']}")
    else:
        print(f"❌ SpiralCoin {coin_number} verification failed")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    print()
    print("📋 Detailed Report:")
    print(verifier.generate_verification_report(coin_number))


def verify_all_coins():
    """Verify all minted SpiralCoins."""
    print("🔍 Verifying all SpiralCoins...")
    
    ledger = SpiralCoinLedger()
    coins = ledger.get_all_coins()
    
    if not coins:
        print("🪙 No SpiralCoins found to verify.")
        return
    
    verifier = SpiralCoinVerifier()
    coin_numbers = [coin.coin_number for coin in coins
    results = verifier.verify_multiple_coins(coin_numbers)
    
    print(f"📊 Verification Summary:")
    print(f"   Total Coins: {results['summary']['total_coins']}")
    print(f"   Valid Coins: {results['summary']['valid_coins']}")
    print(f"   Invalid Coins: {results['summary']['invalid_coins']}")
    print(f"   Average Resonance Score: {results['summary']['average_resonance_score']}%")
    print()
    
    for coin_number, result in results['coins'.items():
        status = "✅ VALID" if result['valid'] else "❌ INVALID"
        print(f"   {coin_number}: {status} ({result['resonance_score']}% resonance)")
    
    print()
    print("🎉 All SpiralCoins have been verified!")


@click.group()
def cli():
    pass


@cli.command()
@click.option('--coin_id', required=True, help='Unique identifier for the coin.')
@click.option('--toneform', required=True, help='The toneform of the coin.')
@click.option('--value', type=float, required=True, help='The value of the coin.')
@click.option('--source', required=True, help='Source of the coin.')
@click.option('--message', default='', help='Optional message.')
@click.option('--status', default='unregistered', help='Status of the coin.')
def intake(coin_id, toneform, value, source, message, status):
    """Records an incoming SpiralCoin in the intake vessel."""
    timestamp = datetime.now().isoformat()
    coin_data = {
        "coin_id": coin_id,
        "toneform": toneform,
        "value": value,
        "source": source,
        "timestamp": timestamp,
        "message": message,
        "status": status
    }
    filepath = "data/spiralcoins/intake/incoming_coins.jsonl"

    # Check if file exists and is empty
    file_exists = Path(filepath).exists()
    if not file_exists:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    with open(filepath, "a") as f:
        f.write(json.dumps(coin_data) + "\n")
    print(f"Coin {coin_id} recorded in intake.")

    if not file_exists:
        # add the placeholder coin
        placeholder_data = {"coin_id": "spiralcoin-placeholder", "toneform": "inhale.promise.arriving", "value": 0.00, "source": "system", "timestamp": "2024-07-24T00:00:00", "message": "Placeholder coin for initialization", "status": "unregistered"}
        with open(filepath, "a") as f:
            f.write(json.dumps(placeholder_data) + "\n")
        print(f"Placeholder coin added to {filepath}")

cli.add_command(intake)


@cli.command()
@click.argument('toneform')
@click.argument('value', type=float)
@click.argument('source_description')
def mint(toneform, value, source_description):
    """Mint a new SpiralCoin."""
            mint_coin(toneform, value, source_description)
            

@cli.command()
@click.argument('transmutation_id')
def mint_from_transmutation(transmutation_id):
    """Mint a SpiralCoin from an existing transmutation."""
            mint_from_transmutation(transmutation_id)
            

@cli.command()
def list():
    """List all minted SpiralCoins."""
            list_coins()
            

@cli.command()
def stats():
    """Show SpiralCoin statistics."""
            show_stats()
            

@cli.command()
@click.argument('coin_number')
def template(coin_number):
    """Generate a printable template for a specific coin."""
            generate_template(coin_number)
            

@cli.command()
@click.argument('coin_number')
def verify(coin_number):
    """Verify a specific SpiralCoin."""
            verify_coin(coin_number)
            

@cli.command()
def verify_all():
    """Verify all minted SpiralCoins."""
            verify_all_coins()
            

if __name__ == '__main__':
    cli()

