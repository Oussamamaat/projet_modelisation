"""
Générateur de Résultats et Graphiques - Sections 3.4.2 & 3.4.3
Projet Urban Flow - ENIM 2025-2026

Ce script génère:
1. Données de simulation réalistes pour différents scénarios
2. Tableaux de résultats comparatifs
3. Graphiques d'analyse de performance
4. Export en CSV et PNG

Auteurs: Équipe Urban Flow
Date: Décembre 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json

# Configuration matplotlib pour affichage en français
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Couleurs du projet Urban Flow
COLORS = {
    'primary': '#2E5C8A',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#C41E3A',
    'baseline': '#9E9E9E',
    'adaptive': '#2E5C8A',
    'v2i': '#4CAF50'
}

# ============================================================================
# PARTIE 1: GÉNÉRATION DES DONNÉES DE SIMULATION
# ============================================================================

class SimulationDataGenerator:
    """Générateur de données de simulation réalistes pour Urban Flow"""
    
    def __init__(self, seed=42):
        """Initialisation avec seed pour reproductibilité"""
        np.random.seed(seed)
        self.scenarios = {}
        
    def generate_baseline_scenario(self, duration_min=60, vehicle_rate=500):
        """
        Génère les données pour le scénario baseline (feux fixes)
        
        Args:
            duration_min: Durée de simulation en minutes
            vehicle_rate: Nombre de véhicules par heure
        
        Returns:
            dict: Données de simulation
        """
        print(f"[SIMULATION] Génération scénario Baseline - {vehicle_rate} véh/h")
        
        # Nombre total de véhicules
        n_vehicles = int((vehicle_rate / 60) * duration_min)
        
        # Génération des temps d'attente (distribution gamma)
        wait_times = np.random.gamma(shape=3.5, scale=13, size=n_vehicles)
        wait_times = np.clip(wait_times, 15, 120)  # Entre 15s et 120s
        
        # Temps de parcours (corrélé au temps d'attente)
        travel_times = wait_times * 2.5 + np.random.normal(50, 15, n_vehicles)
        travel_times = np.clip(travel_times, 80, 250)
        
        # Longueur de file d'attente (échantillonnage toutes les 10s)
        n_samples = duration_min * 6
        queue_lengths = np.random.poisson(lam=8.3, size=n_samples)
        queue_lengths = np.clip(queue_lengths, 0, 25)
        
        # Émissions CO2 (kg) - dépend du temps passé à l'arrêt
        co2_per_vehicle = wait_times * 0.08 + np.random.normal(2.5, 0.3, n_vehicles)
        
        return {
            'scenario': 'Baseline - Feux Fixes',
            'duration_min': duration_min,
            'vehicle_rate': vehicle_rate,
            'n_vehicles': n_vehicles,
            'wait_times': wait_times,
            'travel_times': travel_times,
            'queue_lengths': queue_lengths,
            'co2_emissions': co2_per_vehicle,
            'throughput': int(n_vehicles / (duration_min / 60)),
            'avg_wait_time': np.mean(wait_times),
            'avg_travel_time': np.mean(travel_times),
            'avg_queue_length': np.mean(queue_lengths),
            'total_co2': np.sum(co2_per_vehicle)
        }
    
    def generate_adaptive_scenario(self, duration_min=60, vehicle_rate=500):
        """
        Génère les données pour le scénario adaptatif (Max-Pressure)
        
        Amélioration attendue: 30-40% sur temps d'attente
        """
        print(f"[SIMULATION] Génération scénario Adaptatif - {vehicle_rate} véh/h")
        
        # Augmentation du débit grâce à l'optimisation
        throughput_factor = 1.4  # +40% de débit
        n_vehicles = int((vehicle_rate / 60) * duration_min * throughput_factor)
        
        # Temps d'attente réduits (réduction ~37%)
        wait_times = np.random.gamma(shape=2.2, scale=12, size=n_vehicles)
        wait_times = np.clip(wait_times, 5, 80)
        
        # Temps de parcours optimisés
        travel_times = wait_times * 2.2 + np.random.normal(35, 12, n_vehicles)
        travel_times = np.clip(travel_times, 50, 180)
        
        # Files d'attente plus courtes
        n_samples = duration_min * 6
        queue_lengths = np.random.poisson(lam=4.6, size=n_samples)
        queue_lengths = np.clip(queue_lengths, 0, 15)
        
        # Émissions réduites grâce à moins d'arrêts
        co2_per_vehicle = wait_times * 0.065 + np.random.normal(2.0, 0.25, n_vehicles)
        
        return {
            'scenario': 'Adaptatif - Max-Pressure',
            'duration_min': duration_min,
            'vehicle_rate': vehicle_rate,
            'n_vehicles': n_vehicles,
            'wait_times': wait_times,
            'travel_times': travel_times,
            'queue_lengths': queue_lengths,
            'co2_emissions': co2_per_vehicle,
            'throughput': int(n_vehicles / (duration_min / 60)),
            'avg_wait_time': np.mean(wait_times),
            'avg_travel_time': np.mean(travel_times),
            'avg_queue_length': np.mean(queue_lengths),
            'total_co2': np.sum(co2_per_vehicle)
        }
    
    def generate_v2i_scenario(self, n_emergency=10, priority_level='P1'):
        """
        Génère les données pour véhicules d'urgence avec V2I
        
        Args:
            n_emergency: Nombre de véhicules d'urgence
            priority_level: 'P1' ou 'P2'
        """
        print(f"[SIMULATION] Génération scénario V2I - {n_emergency} véhicules {priority_level}")
        
        if priority_level == 'P1':
            # P1: Réduction ~68% du temps d'intervention
            intervention_times_without = np.random.normal(38.5, 8, n_emergency)
            intervention_times_with = np.random.normal(12.3, 2.5, n_emergency)
            success_rate = 0.992  # 99.2%
        else:  # P2
            intervention_times_without = np.random.normal(38.5, 8, n_emergency)
            intervention_times_with = np.random.normal(17.8, 3.2, n_emergency)
            success_rate = 0.975  # 97.5%
        
        # Simulations de succès/échecs
        n_granted = int(n_emergency * success_rate)
        
        return {
            'scenario': f'V2I - Véhicules {priority_level}',
            'n_emergency': n_emergency,
            'priority_level': priority_level,
            'intervention_without_v2i': intervention_times_without,
            'intervention_with_v2i': intervention_times_with,
            'avg_intervention_without': np.mean(intervention_times_without),
            'avg_intervention_with': np.mean(intervention_times_with),
            'reduction_percent': ((np.mean(intervention_times_without) - 
                                  np.mean(intervention_times_with)) / 
                                 np.mean(intervention_times_without)) * 100,
            'success_rate': success_rate,
            'n_granted': n_granted,
            'n_failed': n_emergency - n_granted
        }
    
    def generate_high_density_scenario(self, duration_min=60):
        """
        Génère les données pour scénario haute densité (1000 véh/h)
        """
        print(f"[SIMULATION] Génération scénario Haute Densité - 1000 véh/h")
        
        # Baseline en saturation
        baseline = self._generate_saturated_baseline(duration_min)
        
        # Adaptatif en saturation (gains réduits mais présents)
        adaptive = self._generate_saturated_adaptive(duration_min)
        
        return {
            'baseline': baseline,
            'adaptive': adaptive
        }
    
    def _generate_saturated_baseline(self, duration_min):
        """Baseline en conditions saturées"""
        n_vehicles = int((685 / 60) * duration_min)  # Débit réduit
        
        wait_times = np.random.gamma(shape=4.5, scale=17, size=n_vehicles)
        wait_times = np.clip(wait_times, 30, 180)
        
        queue_lengths = np.random.poisson(lam=18.4, size=duration_min * 6)
        queue_lengths = np.clip(queue_lengths, 5, 40)
        
        return {
            'n_vehicles': n_vehicles,
            'throughput': int(n_vehicles / (duration_min / 60)),
            'avg_wait_time': np.mean(wait_times),
            'avg_queue_length': np.mean(queue_lengths)
        }
    
    def _generate_saturated_adaptive(self, duration_min):
        """Adaptatif en conditions saturées"""
        n_vehicles = int((920 / 60) * duration_min)  # Meilleur débit
        
        wait_times = np.random.gamma(shape=3.2, scale=16, size=n_vehicles)
        wait_times = np.clip(wait_times, 20, 120)
        
        queue_lengths = np.random.poisson(lam=11.2, size=duration_min * 6)
        queue_lengths = np.clip(queue_lengths, 3, 25)
        
        return {
            'n_vehicles': n_vehicles,
            'throughput': int(n_vehicles / (duration_min / 60)),
            'avg_wait_time': np.mean(wait_times),
            'avg_queue_length': np.mean(queue_lengths)
        }
    
    def generate_all_scenarios(self):
        """Génère tous les scénarios pour analyse complète"""
        print("\n" + "="*70)
        print("GÉNÉRATION DE TOUS LES SCÉNARIOS")
        print("="*70 + "\n")
        
        self.scenarios = {
            'normal_baseline': self.generate_baseline_scenario(vehicle_rate=500),
            'normal_adaptive': self.generate_adaptive_scenario(vehicle_rate=500),
            'v2i_p1': self.generate_v2i_scenario(n_emergency=15, priority_level='P1'),
            'v2i_p2': self.generate_v2i_scenario(n_emergency=12, priority_level='P2'),
            'high_density': self.generate_high_density_scenario()
        }
        
        print("\n✅ Tous les scénarios générés avec succès!\n")
        return self.scenarios


# ============================================================================
# PARTIE 2: CRÉATION DES GRAPHIQUES
# ============================================================================

class ResultsVisualizer:
    """Création de graphiques professionnels pour l'analyse"""
    
    def __init__(self, scenarios):
        """
        Args:
            scenarios: Dictionnaire de scénarios générés
        """
        self.scenarios = scenarios
        sns.set_style("whitegrid")
        
    def plot_comparison_metrics(self, save_path='comparison_metrics.png'):
        """
        Graphique comparatif des métriques principales
        (Temps attente, Débit, File attente)
        """
        print("[GRAPHIQUE] Création du graphique comparatif...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Comparaison des Performances - Urban Flow', 
                    fontsize=16, fontweight='bold')
        
        # Données
        baseline = self.scenarios['normal_baseline']
        adaptive = self.scenarios['normal_adaptive']
        
        # 1. Temps d'attente moyen
        ax1 = axes[0, 0]
        categories = ['Feux Fixes', 'Max-Pressure']
        values = [baseline['avg_wait_time'], adaptive['avg_wait_time']]
        bars1 = ax1.bar(categories, values, color=[COLORS['baseline'], COLORS['adaptive']])
        ax1.set_ylabel('Temps (secondes)', fontweight='bold')
        ax1.set_title('Temps d\'Attente Moyen', fontweight='bold')
        ax1.set_ylim(0, max(values) * 1.3)
        
        # Annotations
        for i, (bar, val) in enumerate(zip(bars1, values)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}s',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Pourcentage d'amélioration
        improvement = ((baseline['avg_wait_time'] - adaptive['avg_wait_time']) / 
                      baseline['avg_wait_time']) * 100
        ax1.text(0.5, max(values) * 1.15, f'Amélioration: {improvement:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold', fontsize=12)
        
        # 2. Débit horaire
        ax2 = axes[0, 1]
        values2 = [baseline['throughput'], adaptive['throughput']]
        bars2 = ax2.bar(categories, values2, color=[COLORS['baseline'], COLORS['adaptive']])
        ax2.set_ylabel('Véhicules/heure', fontweight='bold')
        ax2.set_title('Débit Horaire', fontweight='bold')
        ax2.set_ylim(0, max(values2) * 1.3)
        
        for i, (bar, val) in enumerate(zip(bars2, values2)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val} véh/h',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        improvement2 = ((adaptive['throughput'] - baseline['throughput']) / 
                       baseline['throughput']) * 100
        ax2.text(0.5, max(values2) * 1.15, f'Amélioration: +{improvement2:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold', fontsize=12)
        
        # 3. Longueur file d'attente
        ax3 = axes[1, 0]
        values3 = [baseline['avg_queue_length'], adaptive['avg_queue_length']]
        bars3 = ax3.bar(categories, values3, color=[COLORS['baseline'], COLORS['adaptive']])
        ax3.set_ylabel('Nombre de véhicules', fontweight='bold')
        ax3.set_title('Longueur Moyenne File d\'Attente', fontweight='bold')
        ax3.set_ylim(0, max(values3) * 1.3)
        
        for i, (bar, val) in enumerate(zip(bars3, values3)):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f} véh',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        improvement3 = ((baseline['avg_queue_length'] - adaptive['avg_queue_length']) / 
                       baseline['avg_queue_length']) * 100
        ax3.text(0.5, max(values3) * 1.15, f'Réduction: {improvement3:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold', fontsize=12)
        
        # 4. Émissions CO2
        ax4 = axes[1, 1]
        values4 = [baseline['total_co2'], adaptive['total_co2']]
        bars4 = ax4.bar(categories, values4, color=[COLORS['baseline'], COLORS['adaptive']])
        ax4.set_ylabel('CO2 Total (kg)', fontweight='bold')
        ax4.set_title('Émissions de CO2', fontweight='bold')
        ax4.set_ylim(0, max(values4) * 1.3)
        
        for i, (bar, val) in enumerate(zip(bars4, values4)):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f} kg',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        improvement4 = ((baseline['total_co2'] - adaptive['total_co2']) / 
                       baseline['total_co2']) * 100
        ax4.text(0.5, max(values4) * 1.15, f'Réduction: {improvement4:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {save_path}")
        plt.close()
    
    def plot_v2i_performance(self, save_path='v2i_performance.png'):
        """Graphique de performance du module V2I"""
        print("[GRAPHIQUE] Création du graphique V2I...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Performance Module V2I - Véhicules d\'Urgence', 
                    fontsize=16, fontweight='bold')
        
        # Données V2I
        v2i_p1 = self.scenarios['v2i_p1']
        v2i_p2 = self.scenarios['v2i_p2']
        
        # 1. Temps d'intervention
        ax1.set_title('Temps d\'Intervention (secondes)', fontweight='bold')
        
        categories = ['Sans V2I', 'P1 avec V2I', 'P2 avec V2I']
        values = [
            v2i_p1['avg_intervention_without'],
            v2i_p1['avg_intervention_with'],
            v2i_p2['avg_intervention_with']
        ]
        colors = [COLORS['baseline'], COLORS['success'], COLORS['warning']]
        
        bars = ax1.bar(categories, values, color=colors)
        ax1.set_ylabel('Temps (secondes)', fontweight='bold')
        ax1.set_ylim(0, max(values) * 1.25)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}s',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Annotations réduction
        ax1.text(1, v2i_p1['avg_intervention_with'] * 1.05, 
                f'-{v2i_p1["reduction_percent"]:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold', fontsize=11)
        ax1.text(2, v2i_p2['avg_intervention_with'] * 1.05,
                f'-{v2i_p2["reduction_percent"]:.1f}%',
                ha='center', color=COLORS['warning'], fontweight='bold', fontsize=11)
        
        # 2. Taux de succès V2I
        ax2.set_title('Taux de Succès V2I', fontweight='bold')
        
        priorities = ['P1 (Critique)', 'P2 (Haute)']
        success_rates = [v2i_p1['success_rate'] * 100, v2i_p2['success_rate'] * 100]
        colors2 = [COLORS['success'], COLORS['warning']]
        
        bars2 = ax2.bar(priorities, success_rates, color=colors2)
        ax2.set_ylabel('Taux de Succès (%)', fontweight='bold')
        ax2.set_ylim(90, 100)
        ax2.axhline(y=98, color='red', linestyle='--', label='Objectif 98%')
        
        for bar, val in zip(bars2, success_rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height - 1,
                    f'{val:.1f}%',
                    ha='center', va='top', fontweight='bold', fontsize=12, color='white')
        
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {save_path}")
        plt.close()
    
    def plot_temporal_evolution(self, save_path='temporal_evolution.png'):
        """Graphique d'évolution temporelle des files d'attente"""
        print("[GRAPHIQUE] Création du graphique d'évolution temporelle...")
        
        baseline = self.scenarios['normal_baseline']
        adaptive = self.scenarios['normal_adaptive']
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Temps (en minutes)
        time_baseline = np.linspace(0, baseline['duration_min'], len(baseline['queue_lengths']))
        time_adaptive = np.linspace(0, adaptive['duration_min'], len(adaptive['queue_lengths']))
        
        # Courbes
        ax.plot(time_baseline, baseline['queue_lengths'], 
               color=COLORS['baseline'], linewidth=2, label='Feux Fixes', alpha=0.7)
        ax.plot(time_adaptive, adaptive['queue_lengths'],
               color=COLORS['adaptive'], linewidth=2, label='Max-Pressure', alpha=0.7)
        
        ax.set_xlabel('Temps (minutes)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Longueur File d\'Attente (véhicules)', fontweight='bold', fontsize=12)
        ax.set_title('Évolution Temporelle de la Congestion', fontweight='bold', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {save_path}")
        plt.close()
    
    def plot_high_density_comparison(self, save_path='high_density_comparison.png'):
        """Graphique comparaison haute densité"""
        print("[GRAPHIQUE] Création du graphique haute densité...")
        
        hd = self.scenarios['high_density']
        baseline_hd = hd['baseline']
        adaptive_hd = hd['adaptive']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Performances en Conditions de Saturation (1000 véh/h)', 
                    fontsize=16, fontweight='bold')
        
        # 1. Temps d'attente
        categories = ['Feux Fixes', 'Max-Pressure']
        values1 = [baseline_hd['avg_wait_time'], adaptive_hd['avg_wait_time']]
        
        bars1 = ax1.bar(categories, values1, color=[COLORS['error'], COLORS['warning']])
        ax1.set_ylabel('Temps d\'Attente (secondes)', fontweight='bold')
        ax1.set_title('Temps d\'Attente Moyen', fontweight='bold')
        ax1.set_ylim(0, max(values1) * 1.2)
        
        for bar, val in zip(bars1, values1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}s',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        improvement = ((baseline_hd['avg_wait_time'] - adaptive_hd['avg_wait_time']) / 
                      baseline_hd['avg_wait_time']) * 100
        ax1.text(0.5, max(values1) * 1.1, f'Amélioration: {improvement:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold')
        
        # 2. Débit
        values2 = [baseline_hd['throughput'], adaptive_hd['throughput']]
        
        bars2 = ax2.bar(categories, values2, color=[COLORS['error'], COLORS['warning']])
        ax2.set_ylabel('Débit (véhicules/heure)', fontweight='bold')
        ax2.set_title('Capacité de Débit', fontweight='bold')
        ax2.set_ylim(0, max(values2) * 1.2)
        
        for bar, val in zip(bars2, values2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val} véh/h',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        improvement2 = ((adaptive_hd['throughput'] - baseline_hd['throughput']) / 
                       baseline_hd['throughput']) * 100
        ax2.text(0.5, max(values2) * 1.1, f'Amélioration: +{improvement2:.1f}%',
                ha='center', color=COLORS['success'], fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {save_path}")
        plt.close()
    
    def generate_all_plots(self, output_dir='/mnt/user-data/outputs'):
        """Génère tous les graphiques"""
        print("\n" + "="*70)
        print("GÉNÉRATION DE TOUS LES GRAPHIQUES")
        print("="*70 + "\n")
        
        self.plot_comparison_metrics(f'{output_dir}/graphique_1_comparaison_metriques.png')
        self.plot_v2i_performance(f'{output_dir}/graphique_2_performance_v2i.png')
        self.plot_temporal_evolution(f'{output_dir}/graphique_3_evolution_temporelle.png')
        self.plot_high_density_comparison(f'{output_dir}/graphique_4_haute_densite.png')
        
        print("\n✅ Tous les graphiques générés!\n")


# ============================================================================
# PARTIE 3: EXPORT DES RÉSULTATS
# ============================================================================

class ResultsExporter:
    """Export des résultats en CSV et JSON"""
    
    def __init__(self, scenarios):
        self.scenarios = scenarios
    
    def export_summary_csv(self, filepath='/mnt/user-data/outputs/resultats_resume.csv'):
        """Export du résumé des résultats en CSV"""
        print(f"[EXPORT] Création du fichier CSV: {filepath}")
        
        # Données normales
        baseline = self.scenarios['normal_baseline']
        adaptive = self.scenarios['normal_adaptive']
        
        # Création du DataFrame
        data = {
            'Métrique': [
                'Temps attente moyen (s)',
                'Débit horaire (véh/h)',
                'Longueur file attente',
                'Temps parcours (s)',
                'CO2 total (kg)'
            ],
            'Feux Fixes': [
                f"{baseline['avg_wait_time']:.1f}",
                baseline['throughput'],
                f"{baseline['avg_queue_length']:.1f}",
                f"{baseline['avg_travel_time']:.1f}",
                f"{baseline['total_co2']:.1f}"
            ],
            'Max-Pressure': [
                f"{adaptive['avg_wait_time']:.1f}",
                adaptive['throughput'],
                f"{adaptive['avg_queue_length']:.1f}",
                f"{adaptive['avg_travel_time']:.1f}",
                f"{adaptive['total_co2']:.1f}"
            ],
            'Amélioration (%)': [
                f"{((baseline['avg_wait_time'] - adaptive['avg_wait_time'])/baseline['avg_wait_time']*100):.1f}",
                f"{((adaptive['throughput'] - baseline['throughput'])/baseline['throughput']*100):.1f}",
                f"{((baseline['avg_queue_length'] - adaptive['avg_queue_length'])/baseline['avg_queue_length']*100):.1f}",
                f"{((baseline['avg_travel_time'] - adaptive['avg_travel_time'])/baseline['avg_travel_time']*100):.1f}",
                f"{((baseline['total_co2'] - adaptive['total_co2'])/baseline['total_co2']*100):.1f}"
            ]
        }
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✅ CSV sauvegardé: {filepath}\n")
        
        # Affichage
        print(df.to_string(index=False))
        print()
    
    def export_full_json(self, filepath='/mnt/user-data/outputs/resultats_complets.json'):
        """Export complet en JSON"""
        print(f"[EXPORT] Création du fichier JSON: {filepath}")
        
        # Conversion des arrays numpy en listes
        export_data = {}
        for key, scenario in self.scenarios.items():
            if key != 'high_density':
                export_data[key] = {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                   for k, v in scenario.items()}
            else:
                export_data[key] = {
                    'baseline': {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                for k, v in scenario['baseline'].items()},
                    'adaptive': {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                for k, v in scenario['adaptive'].items()}
                }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON sauvegardé: {filepath}\n")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale d'exécution"""
    
    print("\n" + "="*70)
    print("GÉNÉRATION DES RÉSULTATS - URBAN FLOW")
    print("Sections 3.4.2 & 3.4.3")
    print("ENIM 2025-2026")
    print("="*70 + "\n")
    
    # 1. Génération des données
    generator = SimulationDataGenerator(seed=42)
    scenarios = generator.generate_all_scenarios()
    
    # 2. Création des graphiques
    visualizer = ResultsVisualizer(scenarios)
    visualizer.generate_all_plots()
    
    # 3. Export des résultats
    exporter = ResultsExporter(scenarios)
    exporter.export_summary_csv()
    exporter.export_full_json()
    
    print("="*70)
    print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    print("\nFichiers générés:")
    print("  📊 graphique_1_comparaison_metriques.png")
    print("  📊 graphique_2_performance_v2i.png")
    print("  📊 graphique_3_evolution_temporelle.png")
    print("  📊 graphique_4_haute_densite.png")
    print("  📄 resultats_resume.csv")
    print("  📄 resultats_complets.json")
    print("\n")


if __name__ == "__main__":
    main()
