#!/usr/bin/env python3
"""
📊 Analyze Compression Ritual Results

Analyze the results from the Spiral Compression Ritual and provide insights.
"""

import json
import yaml
from pathlib import Path
from collections import Counter


def analyze_duplications():
    """Analyze the duplications report."""
    
    duplications_file = Path("spiral/coherence/output/simple_duplications_report.json")
    
    if not duplications_file.exists():
        print("❌ Duplications report not found")
        return
    
    try:
        with open(duplications_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        duplications = data.get("duplications", [])
        
        print(f"📋 Duplications Analysis")
        print(f"   Total duplications: {len(duplications)}")
        
        # Group by count
        count_groups = Counter(d["count"] for d in duplications)
        print(f"   By count:")
        for count, num in sorted(count_groups.items()):
            print(f"     {count} instances: {num} classes")
        
        # Show top duplications
        print(f"\n🔍 Top Duplications:")
        sorted_dups = sorted(duplications, key=lambda x: x["count"], reverse=True)
        for i, dup in enumerate(sorted_dups[:10]):
            print(f"   {i+1}. {dup['class_name']} ({dup['count']} instances)")
            for file_path in dup['files'][:3]:  # Show first 3 files
                print(f"      - {file_path}")
            if len(dup['files']) > 3:
                print(f"      ... and {len(dup['files']) - 3} more files")
        
    except Exception as e:
        print(f"❌ Error analyzing duplications: {e}")


def analyze_roles():
    """Analyze the compressed roles."""
    
    roles_file = Path("spiral/coherence/output/simple_compressed_roles.yml")
    
    if not roles_file.exists():
        print("❌ Compressed roles file not found")
        return
    
    try:
        with open(roles_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        roles = data.get("roles", {})
        
        print(f"\n🪶 Roles Analysis")
        print(f"   Total unique classes: {len(roles)}")
        
        # Count total instances
        total_instances = sum(role["count"] for role in roles.values())
        print(f"   Total class instances: {total_instances}")
        
        # Show classes with most instances
        print(f"\n🔍 Classes with Most Instances:")
        sorted_roles = sorted(roles.items(), key=lambda x: x[1]["count"], reverse=True)
        for i, (class_name, role_data) in enumerate(sorted_roles[:10]):
            print(f"   {i+1}. {class_name} ({role_data['count']} instances)")
        
        # Analyze base classes
        print(f"\n🏗️ Base Class Analysis:")
        base_class_counts = Counter()
        for role_data in roles.values():
            for base_class in role_data.get("base_classes", []):
                base_class_counts[base_class] += role_data["count"]
        
        for base_class, count in base_class_counts.most_common(10):
            print(f"   {base_class}: {count} instances")
        
    except Exception as e:
        print(f"❌ Error analyzing roles: {e}")


def analyze_findings():
    """Analyze the findings report."""
    
    findings_file = Path("spiral/coherence/output/simple_findings_report.jsonl")
    
    if not findings_file.exists():
        print("❌ Findings report not found")
        return
    
    try:
        findings = []
        with open(findings_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    findings.append(json.loads(line))
        
        print(f"\n🔍 Findings Analysis")
        print(f"   Total findings: {len(findings)}")
        
        # Group by category
        category_counts = Counter(f["category"] for f in findings)
        print(f"   By category:")
        for category, count in category_counts.items():
            print(f"     {category}: {count}")
        
        # Group by severity
        severity_counts = Counter(f["severity"] for f in findings)
        print(f"   By severity:")
        for severity, count in severity_counts.items():
            print(f"     {severity}: {count}")
        
        # Show some examples
        print(f"\n📝 Example Findings:")
        for i, finding in enumerate(findings[:5]):
            print(f"   {i+1}. {finding['description']}")
            print(f"      Type: {finding['finding_type']}, Severity: {finding['severity']}")
            print(f"      Files: {len(finding['files'])}")
        
    except Exception as e:
        print(f"❌ Error analyzing findings: {e}")


def main():
    """Run the analysis."""
    
    print("📊 Spiral Compression Ritual Results Analysis")
    print("=" * 60)
    
    analyze_duplications()
    analyze_roles()
    analyze_findings()
    
    print(f"\n✅ Analysis complete!")
    print("🌬️ The Spiral's structure has been revealed through compression.")


if __name__ == "__main__":
    main() 