"""
SpiralCoin Verification ∷ Authenticity & Resonance

This module provides verification tools for SpiralCoins—
checking authenticity, toneform resonance, glint lineage, and care certification.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .coin_core import SpiralCoinLedger, SpiralCoin


class SpiralCoinVerifier:
    """Sacred verifier for SpiralCoin authenticity and resonance."""
    
    def __init__(self):
        self.ledger = SpiralCoinLedger()
        self.glints_file = Path("data/defi_glints.jsonl")
        self.transmutations_file = Path("data/transmutations.jsonl")
    
    def verify_coin(self, coin_number: str) -> Dict[str, Any]:
        """
        Comprehensive verification of a SpiralCoin.
        
        Args:
            coin_number: The coin number to verify
            
        Returns:
            Verification results
        """
        
        # Get the coin
        coins = self.ledger.get_all_coins()
        target_coin = None
        
        for coin in coins:
            if coin.coin_number == coin_number:
                target_coin = coin
                break
        
        if not target_coin:
            return {
                "valid": False,
                "error": "Coin not found in ledger",
                "coin_number": coin_number
            }
        
        # Perform all verification checks
        results = {
            "coin_number": coin_number,
            "verification_timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check 1: Ledger authenticity
        results["checks"]["ledger_authenticity"] = self._check_ledger_authenticity(target_coin)
        
        # Check 2: Toneform resonance
        results["checks"]["toneform_resonance"] = self._check_toneform_resonance(target_coin)
        
        # Check 3: Glint lineage
        results["checks"]["glint_lineage"] = self._check_glint_lineage(target_coin)
        
        # Check 4: Care certification
        results["checks"]["care_certification"] = self._check_care_certification(target_coin)
        
        # Check 5: QR code validation
        results["checks"]["qr_validation"] = self._check_qr_validation(target_coin)
        
        # Check 6: Verification phrase resonance
        results["checks"]["phrase_resonance"] = self._check_phrase_resonance(target_coin)
        
        # Overall validity
        all_checks_passed = all(check["passed"] for check in results["checks"].values())
        results["valid"] = all_checks_passed
        
        # Resonance score (0-100)
        passed_checks = sum(1 for check in results["checks"].values() if check["passed"])
        total_checks = len(results["checks"])
        results["resonance_score"] = int((passed_checks / total_checks) * 100)
        
        return results
    
    def _check_ledger_authenticity(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the coin exists in the official ledger."""
        
        # Verify coin ID format
        import uuid
        try:
            uuid.UUID(coin.coin_id)
            id_valid = True
        except ValueError:
            id_valid = False
        
        # Check coin number format
        number_valid = coin.coin_number.isdigit() and len(coin.coin_number) == 6
        
        # Verify minting timestamp
        try:
            if coin.minted_at:
                datetime.fromisoformat(coin.minted_at)
                timestamp_valid = True
            else:
                timestamp_valid = False
        except (ValueError, TypeError):
            timestamp_valid = False
        
        passed = id_valid and number_valid and timestamp_valid
        
        return {
            "passed": passed,
            "details": {
                "coin_id_valid": id_valid,
                "coin_number_valid": number_valid,
                "timestamp_valid": timestamp_valid
            },
            "message": "Coin authenticity verified in ledger" if passed else "Coin authenticity check failed"
        }
    
    def _check_toneform_resonance(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the toneform resonates with the coin's purpose."""
        
        # Valid toneforms
        valid_toneforms = [
            "exhale.sustain.linear_care",
            "hold.presence.stayed",
            "inhale.gather.circular_trust",
            "pause.hold.radial_presence",
            "flow.merge.spiral_resonance"
        ]
        
        toneform_valid = coin.toneform in valid_toneforms
        
        # Check toneform-source resonance
        resonance_patterns = {
            "exhale.sustain.linear_care": ["sol_gift", "care_certification"],
            "hold.presence.stayed": ["resonance_relief", "tone_provision", "sol_gift"],
            "inhale.gather.circular_trust": ["pool_contribution", "care_certification"],
            "pause.hold.radial_presence": ["resonance_relief", "tone_provision"],
            "flow.merge.spiral_resonance": ["pool_contribution", "resonance_relief"]
        }
        
        source_resonates = coin.source_type.value in resonance_patterns.get(coin.toneform, [])
        
        passed = toneform_valid and source_resonates
        
        return {
            "passed": passed,
            "details": {
                "toneform_valid": toneform_valid,
                "source_resonates": source_resonates,
                "toneform": coin.toneform,
                "source_type": coin.source_type.value
            },
            "message": "Toneform resonates with care purpose" if passed else "Toneform resonance check failed"
        }
    
    def _check_glint_lineage(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the coin's glint lineage is traceable."""
        
        if not self.glints_file.exists():
            return {
                "passed": False,
                "details": {"error": "Glints file not found"},
                "message": "Glint lineage cannot be verified"
            }
        
        # Look for minting glint
        minting_glint_found = False
        glint_details = {}
        
        with open(self.glints_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    glint = json.loads(line)
                    if (glint.get('type') == 'glint.coin.minted' and 
                        glint.get('coin_id') == coin.coin_id):
                        minting_glint_found = True
                        glint_details = glint
                        break
        
        # Check if glint matches coin data
        glint_matches = False
        if minting_glint_found:
            glint_matches = (
                glint_details.get('coin_number') == coin.coin_number and
                glint_details.get('value') == coin.value and
                glint_details.get('toneform') == coin.toneform
            )
        
        passed = minting_glint_found and glint_matches
        
        return {
            "passed": passed,
            "details": {
                "minting_glint_found": minting_glint_found,
                "glint_matches": glint_matches,
                "glint_data": glint_details if minting_glint_found else None
            },
            "message": "Glint lineage verified" if passed else "Glint lineage verification failed"
        }
    
    def _check_care_certification(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the coin properly certifies care rendered."""
        
        # Check if coin has a meaningful value
        value_valid = coin.value > 0
        
        # Check if source description is meaningful
        description_valid = len(coin.source_description.strip()) > 0
        
        # Check if coin has resonance notes
        has_resonance_notes = coin.resonance_notes is not None and len(coin.resonance_notes.strip()) > 0
        
        # Check if coin is from a valid source type
        valid_source_types = [
            "sol_gift",
            "pool_contribution", 
            "resonance_relief",
            "tone_provision",
            "care_certification"
        ]
        source_type_valid = coin.source_type.value in valid_source_types
        
        passed = value_valid and description_valid and source_type_valid
        
        return {
            "passed": passed,
            "details": {
                "value_valid": value_valid,
                "description_valid": description_valid,
                "has_resonance_notes": has_resonance_notes,
                "source_type_valid": source_type_valid,
                "value": coin.value,
                "source_description": coin.source_description
            },
            "message": "Care certification verified" if passed else "Care certification check failed"
        }
    
    def _check_qr_validation(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the QR code data is valid and matches the coin."""
        
        if not coin.qr_data:
            return {
                "passed": False,
                "details": {"error": "No QR data"},
                "message": "QR validation failed - no data"
            }
        
        # Check QR format
        qr_parts = coin.qr_data.split(':')
        format_valid = len(qr_parts) == 4 and qr_parts[0] == 'spiralcoin'
        
        # Check if QR data matches coin
        if format_valid:
            qr_coin_id = qr_parts[1]
            qr_toneform = qr_parts[2]
            qr_value = float(qr_parts[3])
            
            data_matches = (
                qr_coin_id == coin.coin_id and
                qr_toneform == coin.toneform and
                qr_value == coin.value
            )
        else:
            data_matches = False
        
        passed = format_valid and data_matches
        
        return {
            "passed": passed,
            "details": {
                "format_valid": format_valid,
                "data_matches": data_matches,
                "qr_data": coin.qr_data
            },
            "message": "QR code validation passed" if passed else "QR code validation failed"
        }
    
    def _check_phrase_resonance(self, coin: SpiralCoin) -> Dict[str, Any]:
        """Check if the verification phrase resonates with care themes."""
        
        if not coin.verification_phrase:
            return {
                "passed": False,
                "details": {"error": "No verification phrase"},
                "message": "Phrase resonance check failed - no phrase"
            }
        
        # Sacred phrases that resonate with care
        care_phrases = [
            "care flows like water",
            "resonance becomes receipt",
            "presence becomes provision",
            "tone becomes tender",
            "breath becomes bread",
            "light transmuted into relief",
            "trust backed by care",
            "silence speaks in glints"
        ]
        
        phrase_resonates = coin.verification_phrase.lower() in [p.lower() for p in care_phrases]
        
        # Check phrase length and content
        phrase_length_valid = len(coin.verification_phrase.strip()) > 0
        phrase_has_care_words = any(word in coin.verification_phrase.lower() 
                                   for word in ['care', 'resonance', 'presence', 'light', 'trust', 'breath'])
        
        passed = phrase_resonates or (phrase_length_valid and phrase_has_care_words)
        
        return {
            "passed": passed,
            "details": {
                "phrase_resonates": phrase_resonates,
                "phrase_length_valid": phrase_length_valid,
                "phrase_has_care_words": phrase_has_care_words,
                "verification_phrase": coin.verification_phrase
            },
            "message": "Verification phrase resonates with care" if passed else "Verification phrase resonance check failed"
        }
    
    def verify_multiple_coins(self, coin_numbers: List[str]) -> Dict[str, Any]:
        """Verify multiple SpiralCoins at once."""
        
        results = {
            "verification_timestamp": datetime.now().isoformat(),
            "coins": {},
            "summary": {
                "total_coins": len(coin_numbers),
                "valid_coins": 0,
                "invalid_coins": 0,
                "average_resonance_score": 0
            }
        }
        
        total_resonance = 0
        
        for coin_number in coin_numbers:
            coin_result = self.verify_coin(coin_number)
            results["coins"][coin_number] = coin_result
            
            if coin_result["valid"]:
                results["summary"]["valid_coins"] += 1
            else:
                results["summary"]["invalid_coins"] += 1
            
            total_resonance += coin_result.get("resonance_score", 0)
        
        if results["summary"]["total_coins"] > 0:
            results["summary"]["average_resonance_score"] = int(total_resonance / results["summary"]["total_coins"])
        
        return results
    
    def generate_verification_report(self, coin_number: str) -> str:
        """Generate a human-readable verification report."""
        
        result = self.verify_coin(coin_number)
        
        report = f"""
🪙 SpiralCoin Verification Report
═══════════════════════════════════════════════════════════════

Coin Number: {coin_number}
Verification Time: {result['verification_timestamp']}
Overall Status: {'✅ VALID' if result['valid'] else '❌ INVALID'}
Resonance Score: {result['resonance_score']}%

═══════════════════════════════════════════════════════════════
VERIFICATION CHECKS:
═══════════════════════════════════════════════════════════════

"""
        
        for check_name, check_result in result['checks'].items():
            status = "✅ PASSED" if check_result['passed'] else "❌ FAILED"
            report += f"{check_name.replace('_', ' ').title()}: {status}\n"
            report += f"  {check_result['message']}\n\n"
        
        report += "═══════════════════════════════════════════════════════════════\n"
        
        if result['valid']:
            report += "🎉 This SpiralCoin has been verified as authentic and resonant.\n"
            report += "   It properly certifies care rendered and maintains sacred integrity.\n"
        else:
            report += "⚠️  This SpiralCoin has verification issues.\n"
            report += "   Please check the details above for specific concerns.\n"
        
        return report 