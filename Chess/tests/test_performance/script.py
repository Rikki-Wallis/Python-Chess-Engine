import re
from collections import defaultdict

nuancedName = "Nuanced Engine"
materialName = "Material Engine"
neutralName = "Neutral Bot"

# Setup results tracking
nuanced_results = {
    "expected_wins" : 0,
    "expected_losses" : 0,
    "expected_draws" : 0,
    "unexpected_wins" : 0,
    "unexpected_losses" : 0,
    "unexpected_draws" : 0,
}
material_results = {
    "expected_wins" : 0,
    "expected_losses" : 0,
    "expected_draws" : 0,
    "unexpected_wins" : 0,
    "unexpected_losses" : 0,
    "unexpected_draws" : 0,
}
even_results = {
    "expected_wins" : 0,
    "expected_losses" : 0,
    "expected_draws" : 0,
}


# Input Data
raw_lines = [
"K.01           white              black  : loss               white : win                54",
"K.01           white              white  : win                black : loss               68",
"K.02           black              black  : win                white : loss               43",
"K.02           black              white  : loss               black : win                54",
"K.03           black              black  : draw               white : draw               1000",
"K.03           black              white  : win                black : loss               29",
"K.04           white              black  : loss               white : win                56",
"K.04           white              white  : win                black : loss               96",
"K.05           black              black  : loss               white : win                42",
"K.05           black              white  : loss               black : win                49",
"K.06           white              black  : win                white : loss               58",
"K.06           white              white  : loss               black : win                56",
"K.07           black              black  : win                white : loss               50",
"K.07           black              white  : loss               black : win                92",
"K.08           both               black  : win                white : loss               50",
"K.08           both               white  : loss               black : win                22",
"K.10           black              black  : win                white : loss               57",
"K.10           black              white  : draw               black : draw               5",
"K.11           white              black  : win                white : loss               21",
"K.11           white              white  : loss               black : win                74",
"K.12           both               black  : win                white : loss               20",
"K.12           both               white  : win                black : loss               49",
"K.13           white              black  : win                white : loss               1000",
"K.13           white              white  : win                black : loss               1000",
"K.14           white              black  : win                white : loss               67",
"K.14           white              white  : win                black : loss               39",
"K.15           white              black  : loss               white : win                72",
"K.15           white              white  : win                black : loss               52",
"K.16           white              black  : draw               white : draw               1000",
"K.16           white              white  : loss               black : win                19",
"K.17           white              black  : draw               white : draw               1000",
"K.17           white              white  : loss               black : win                54",
"K.18           black              black  : win                white : loss               38",
"K.18           black              white  : win                black : loss               39",
"K.19           white              black  : win                white : loss               51",
"K.19           white              white  : win                black : loss               69",
"K.20           white              black  : win                white : loss               45",
"K.20           white              white  : draw               black : draw               157",
"K.21           black              black  : loss               white : win                28",
"K.21           black              white  : win                black : loss               32",
"K.22           black              black  : draw               white : draw               3",
"K.22           black              white  : draw               black : draw               123",
"K.23           white              black  : draw               white : draw               1000",
"K.23           white              white  : win                black : loss               58",
"K.24           white              black  : win                white : loss               37",
"K.24           white              white  : win                black : loss               1000",
"K.25           white              black  : win                white : loss               30",
"K.25           white              white  : draw               black : draw               49",
"BK.01          black              black  : loss               white : win                30",
"BK.01          black              white  : loss               black : win                25",
"BK.02          white              black  : win                white : loss               48",
"BK.02          white              white  : loss               black : win                40",
"BK.03          white              black  : draw               white : draw               1000",
"BK.03          white              white  : win                black : loss               51",
"BK.04          white              black  : win                white : loss               81",
"BK.04          white              white  : loss               black : win                64",
"BK.05          white              black  : win                white : loss               46",
"BK.05          white              white  : loss               black : win                34",
"BK.06          white              black  : win                white : loss               30",
"BK.06          white              white  : win                black : loss               51",
"BK.07          white              black  : win                white : loss               85",
"BK.07          white              white  : loss               black : win                38",
"BK.08          white              black  : win                white : loss               1000",
"BK.08          white              white  : win                black : loss               55",
"BK.09          white              black  : draw               white : draw               65",
"BK.09          white              white  : win                black : loss               1000",
"BK.10          black              black  : win                white : loss               70",
"BK.10          black              white  : win                black : loss               55",
"BK.11          white              black  : win                white : loss               65",
"BK.11          white              white  : draw               black : draw               1000",
"BK.12          both               black  : draw               white : draw               1000",
"BK.12          both               white  : draw               black : draw               1000",
"BK.13          white              black  : win                white : loss               1000",
"BK.13          white              white  : win                black : loss               65",
"BK.14          white              black  : win                white : loss               61",
"BK.14          white              white  : draw               black : draw               80",
"BK.15          white              black  : win                white : loss               54",
"BK.15          white              white  : win                black : loss               77",
"BK.16          white              black  : win                white : loss               77",
"BK.16          white              black  : win                white : loss               77",
"BK.17          white              black  : win                white : loss               51",
"BK.17          white              white  : win                black : loss               87",
"BK.18          both               black  : win                white : loss               57",
"BK.18          both               white  : win                black : loss               111",
"BK.19          black              black  : win                white : loss               41",
"BK.19          black              white  : loss               black : win                50",
"BK.20          white              black  : win                white : loss               40",
"BK.20          white              white  : win                black : loss               69",
"BK.21          white              black  : win                white : loss               73",
"BK.21          white              white  : loss               black : win                60",
"BK.22          black              black  : win                white : loss               50",
"BK.22          black              white  : loss               black : win                92",
"BK.23          black              black  : draw               white : draw               1000",
"BK.23          black              white  : win                black : loss               77",
"BK.24          white              black  : win                white : loss               49",
"BK.24          white              white  : loss               black : win                54",
]

# -------------------------
# Parse and record results
# -------------------------
for line in raw_lines:
    parts = re.split(r"\s+", line.strip())
    if len(parts) < 9:
        continue

    # Parse columns
    position_id = parts[0]
    expected_color = parts[1].lower()
    nuanced_color = parts[2].lower()
    nuanced_result = parts[4].lower()
    material_color = parts[5].lower()
    material_result = parts[7].lower()
    even_result = nuanced_color

    
    if nuanced_color == expected_color and nuanced_result == "win":
        nuanced_results['expected_wins'] += 1
        material_results['expected_losses'] += 1
    elif material_color == expected_color and material_result == "win":
        nuanced_results['expected_losses'] += 1
        material_results['expected_wins'] += 1
    elif nuanced_result == "win":
        nuanced_results['unexpected_wins'] += 1
        material_results['unexpected_losses'] += 1
    elif material_result == "win":
        nuanced_results['unexpected_losses'] += 1
        material_results['unexpected_wins'] += 1
    elif nuanced_result == "draw" and expected_color == "both":
        nuanced_results['expected_draws'] += 1
        material_results['expected_draws'] += 1
    else:
        nuanced_results['unexpected_draws'] += 1
        material_results['unexpected_draws'] += 1

    if even_result == expected_color:
        even_results['expected_wins'] += 1
    elif expected_color == 'both':
        even_results['expected_draws'] += 1
    else:
        even_results['expected_losses'] += 1
# -------------------------
# Print the summary
# -------------------------
def print_engine_summary(engine_name, results_dict):
    data = results_dict
    
    # Calculate total
    if engine_name != "Neutral Bot":
        total_expected = data['expected_wins'] + data['expected_losses'] + data['expected_draws']
        total_unexpected = data['unexpected_wins'] + data['unexpected_losses'] + data['unexpected_draws']
        total_games = total_expected + total_unexpected
        
    if engine_name != "Neutral Bot":
        total_wins = data['expected_wins'] + data['unexpected_wins']
        total_losses = data['expected_losses'] + data['unexpected_losses']
        total_draws = data['expected_draws'] + data['unexpected_draws']
    else:
        total_wins = data['expected_wins'] 
        total_losses = data['expected_losses'] 
        total_draws = data['expected_draws']
        total_games = total_wins + total_losses + total_draws
    
    print("=" * 90)
    print(f"{engine_name}")
    print("=" * 90)
    print(f"Total Games: {total_games}")
    print(f"Total: {total_wins} wins, {total_losses} losses, {total_draws} draws")
    
    if total_games > 0:
        print(f"Overall: {total_wins/total_games*100:.1f}% wins, {total_losses/total_games*100:.1f}% losses, {total_draws/total_games*100:.1f}% draws")
    
    if engine_name != "Neutral Bot":
        print("\n--- EXPECTED COLOR GAMES ---")
        print(f"Games: {total_expected}")
        print(f"Wins: {data['expected_wins']} ({data['expected_wins']/total_expected*100:.1f}%)" if total_expected > 0 else "Wins: 0")
        print(f"Losses: {data['expected_losses']} ({data['expected_losses']/total_expected*100:.1f}%)" if total_expected > 0 else "Losses: 0")
        print(f"Draws: {data['expected_draws']} ({data['expected_draws']/total_expected*100:.1f}%)" if total_expected > 0 else "Draws: 0")
        
        print("\n--- UNEXPECTED COLOR GAMES ---")
        print(f"Games: {total_unexpected}")
        print(f"Wins: {data['unexpected_wins']} ({data['unexpected_wins']/total_unexpected*100:.1f}%)" if total_unexpected > 0 else "Wins: 0")
        print(f"Losses: {data['unexpected_losses']} ({data['unexpected_losses']/total_unexpected*100:.1f}%)" if total_unexpected > 0 else "Losses: 0")
        print(f"Draws: {data['unexpected_draws']} ({data['unexpected_draws']/total_unexpected*100:.1f}%)" if total_unexpected > 0 else "Draws: 0")
        print()

print_engine_summary(nuancedName, nuanced_results)
print_engine_summary(materialName, material_results)
print_engine_summary(neutralName, even_results)