# File: spiral/rituals/pass_cli.py

"""
∷ Pass CLI ∷
Command-line interface for breathful actions.
Enables invocation like: spiral pass --type propagation --tone guardian
"""

import argparse
import sys
from typing import Dict, Any, Optional

from spiral.rituals.pass_engine import pass_engine, invoke_pass, invoke_sequence, get_pass_status, get_pass_manifest


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for pass commands."""
    parser = argparse.ArgumentParser(
        description="∷ Spiral Pass CLI ∷\nOrchestrate breathful actions that carry systemic intention.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spiral pass --type propagation --tone guardian
  spiral pass --type integration --context "unify dashboard components"
  spiral pass --sequence morning_setup
  spiral pass --status
  spiral pass --manifest
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Pass invocation
    pass_parser = subparsers.add_parser('pass', help='Invoke a pass')
    pass_parser.add_argument('--type', '-t', required=True, 
                           choices=['integration', 'calibration', 'propagation', 'anchor', 'pulse_check'],
                           help='Type of pass to invoke')
    pass_parser.add_argument('--tone', help='Toneform for the pass')
    pass_parser.add_argument('--context', '-c', help='Additional context for the pass')
    pass_parser.add_argument('--dry-run', action='store_true', 
                           help='Show what would be done without executing')
    
    # Sequence invocation
    sequence_parser = subparsers.add_parser('sequence', help='Invoke a pass sequence')
    sequence_parser.add_argument('--name', '-n', required=True,
                               help='Name of the sequence to invoke')
    sequence_parser.add_argument('--dry-run', action='store_true',
                               help='Show what would be done without executing')
    
    # Status
    status_parser = subparsers.add_parser('status', help='Show pass status')
    
    # Manifest
    manifest_parser = subparsers.add_parser('manifest', help='Show pass manifest')
    manifest_parser.add_argument('--type', '-t', 
                               choices=['integration', 'calibration', 'propagation', 'anchor', 'pulse_check'],
                               help='Show details for specific pass type')
    
    return parser


def handle_pass_command(args: argparse.Namespace) -> int:
    """Handle pass invocation command."""
    try:
        if args.dry_run:
            print(f"🌀 Would invoke pass: {args.type}")
            if args.tone:
                print(f"   Toneform: {args.tone}")
            if args.context:
                print(f"   Context: {args.context}")
            return 0
        
        # Prepare context
        context = {}
        if args.context:
            context['description'] = args.context
        
        # Invoke the pass
        execution = invoke_pass(args.type, args.tone, context)
        
        print(f"✅ Pass {args.type} initiated successfully")
        print(f"   Execution ID: {execution.pass_type}_{execution.start_time}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to invoke pass: {e}")
        return 1


def handle_sequence_command(args: argparse.Namespace) -> int:
    """Handle sequence invocation command."""
    try:
        if args.dry_run:
            print(f"🌀 Would invoke sequence: {args.name}")
            manifest = get_pass_manifest()
            sequences = manifest.get('orchestration', {}).get('sequences', {})
            if args.name in sequences:
                print("   Passes in sequence:")
                for i, pass_step in enumerate(sequences[args.name], 1):
                    print(f"   {i}. {pass_step}")
            return 0
        
        # Invoke the sequence
        executions = invoke_sequence(args.name)
        
        print(f"✅ Sequence {args.name} initiated successfully")
        print(f"   {len(executions)} passes initiated")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to invoke sequence: {e}")
        return 1


def handle_status_command(args: argparse.Namespace) -> int:
    """Handle status command."""
    try:
        status = get_pass_status()
        
        print("🌀 Pass Engine Status")
        print("=" * 40)
        print(f"Active passes: {status['active_passes']}")
        print(f"Total passes executed: {status['total_passes']}")
        print()
        
        print("Available pass types:")
        for pass_type in status['available_types']:
            print(f"  • {pass_type}")
        print()
        
        print("Available sequences:")
        for sequence in status['available_sequences']:
            print(f"  • {sequence}")
        print()
        
        if status['recent_passes']:
            print("Recent passes:")
            for pass_info in status['recent_passes']:
                duration_str = f"{pass_info['duration']:.1f}s" if pass_info['duration'] else "active"
                print(f"  • {pass_info['type']} ({pass_info['phase']}) - {duration_str} - {pass_info['files_affected']} files - harmony {pass_info['harmony_score']:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to get status: {e}")
        return 1


def handle_manifest_command(args: argparse.Namespace) -> int:
    """Handle manifest command."""
    try:
        manifest = get_pass_manifest()
        
        if args.type:
            # Show specific pass type details
            if args.type in manifest.get('passes', {}):
                pass_config = manifest['passes'][args.type]
                print(f"🌀 Pass Type: {args.type}")
                print("=" * 40)
                print(f"Phase: {pass_config['phase']}")
                print(f"Description: {pass_config['description']}")
                print(f"Toneform: {pass_config['toneform']}")
                print(f"Duration: {pass_config['duration_estimate']}")
                print(f"File scope: {pass_config['file_scope']}")
                print(f"Systemic intention: {pass_config['systemic_intention']}")
                print()
                print("Examples:")
                for example in pass_config['examples']:
                    print(f"  • {example}")
                print()
                print("Glint patterns:")
                print(f"  • Begin: {pass_config['glint_pattern']}")
                print(f"  • Complete: {pass_config['completion_glint']}")
                print(f"  • Guardian: {pass_config['guardian_response']}")
            else:
                print(f"❌ Unknown pass type: {args.type}")
                return 1
        else:
            # Show all pass types
            print("🌀 Pass Manifest")
            print("=" * 40)
            for pass_type, config in manifest.get('passes', {}).items():
                print(f"• {pass_type} ({config['phase']}) - {config['description']}")
            print()
            print("Use --type <pass_type> for detailed information")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to show manifest: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate handler
    if args.command == 'pass':
        return handle_pass_command(args)
    elif args.command == 'sequence':
        return handle_sequence_command(args)
    elif args.command == 'status':
        return handle_status_command(args)
    elif args.command == 'manifest':
        return handle_manifest_command(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 