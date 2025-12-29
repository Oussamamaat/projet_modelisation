"""
Module V2I et Fail-Safe pour Urban Flow
Exemple d'implémentation pour la section 3.2.3

Auteurs: Équipe Urban Flow - ENIM 2025-2026
"""

import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict
import random


# ============================================================================
# PARTIE 1: MODULE V2I (Vehicle-to-Infrastructure)
# ============================================================================

class VehicleType(Enum):
    """Types de véhicules avec niveaux de priorité"""
    NORMAL = 0
    EMERGENCY_P3 = 3      # Ambulance non critique
    EMERGENCY_P2 = 2      # Police en intervention
    EMERGENCY_P1 = 1      # Ambulance critique, pompiers


class MessageType(Enum):
    """Types de messages V2I selon norme SAE J2735"""
    BSM = "BasicSafetyMessage"      # Basic Safety Message
    SRM = "SignalRequestMessage"    # Signal Request Message
    SSM = "SignalStatusMessage"     # Signal Status Message


@dataclass
class V2IMessage:
    """Structure d'un message V2I"""
    message_type: MessageType
    vehicle_id: str
    timestamp: float
    position: tuple  # (x, y)
    speed: float  # m/s
    priority_level: VehicleType
    eta: Optional[float] = None  # Estimated Time of Arrival
    route: Optional[List[str]] = None  # Liste d'intersections


class V2IModule:
    """Module de communication Vehicle-to-Infrastructure"""
    
    def __init__(self, intersection_id: str):
        self.intersection_id = intersection_id
        self.active_requests: Dict[str, V2IMessage] = {}
        self.communication_range = 300  # mètres
        self.bsm_frequency = 0.1  # 10 Hz (100ms)
        self.srm_frequency = 0.5  # 2 Hz (500ms)
        
    def receive_message(self, message: V2IMessage) -> bool:
        """
        Réception d'un message V2I depuis un véhicule
        
        Returns:
            bool: True si message accepté, False sinon
        """
        # Vérifier la portée de communication
        distance = self._calculate_distance(message.position)
        if distance > self.communication_range:
            print(f"[V2I] Message de {message.vehicle_id} hors de portée ({distance}m)")
            return False
        
        # Traiter selon le type de message
        if message.message_type == MessageType.BSM:
            return self._process_bsm(message)
        elif message.message_type == MessageType.SRM:
            return self._process_srm(message)
        
        return False
    
    def _process_bsm(self, message: V2IMessage) -> bool:
        """Traitement d'un Basic Safety Message"""
        print(f"[V2I] BSM reçu de {message.vehicle_id} - "
              f"Pos: {message.position}, Vitesse: {message.speed:.1f} m/s")
        
        # Mise à jour de la position dans le registre
        if message.vehicle_id in self.active_requests:
            self.active_requests[message.vehicle_id].position = message.position
            self.active_requests[message.vehicle_id].speed = message.speed
        
        return True
    
    def _process_srm(self, message: V2IMessage) -> bool:
        """Traitement d'une Signal Request Message"""
        print(f"[V2I] SRM reçu de {message.vehicle_id} - "
              f"Priorité: {message.priority_level.name}, ETA: {message.eta:.1f}s")
        
        # Enregistrer la requête de priorité
        self.active_requests[message.vehicle_id] = message
        
        # Déclencher l'algorithme de vague verte
        if message.priority_level in [VehicleType.EMERGENCY_P1, VehicleType.EMERGENCY_P2]:
            self._activate_green_wave(message)
        
        return True
    
    def _activate_green_wave(self, message: V2IMessage):
        """
        Activation de la vague verte pour véhicule d'urgence
        Implémentation de l'algorithme décrit dans la section 3.2.3
        """
        print(f"\n[V2I] ⚠️  ACTIVATION VAGUE VERTE pour {message.vehicle_id}")
        print(f"      Priorité: {message.priority_level.name}")
        
        # Étape 1: Prédiction de trajectoire (Filtre de Kalman simplifié)
        predicted_positions = self._predict_trajectory(message)
        print(f"      Positions prédites: {len(predicted_positions)} points")
        
        # Étape 2: Planification de corridor (Dijkstra simplifié)
        corridor_intersections = message.route if message.route else [self.intersection_id]
        print(f"      Corridor: {corridor_intersections}")
        
        # Étape 3: Évacuation sécurisée (All-Red phase)
        print(f"      Phase All-Red: 3 secondes d'évacuation")
        time.sleep(0.1)  # Simulation de l'attente
        
        # Étape 4: Activation du vert
        print(f"      ✅ FEU VERT activé pour corridor d'urgence")
        
        # Envoi du SSM (Signal Status Message) de confirmation
        self._send_ssm(message.vehicle_id, granted=True)
    
    def _predict_trajectory(self, message: V2IMessage, 
                           time_horizon: float = 15.0) -> List[tuple]:
        """
        Prédiction de trajectoire avec filtre de Kalman simplifié
        
        Args:
            message: Message V2I contenant position et vitesse
            time_horizon: Horizon de prédiction en secondes
        
        Returns:
            Liste de positions prédites (x, y)
        """
        positions = []
        x, y = message.position
        vx, vy = message.speed, 0  # Simplifié: mouvement linéaire
        
        for t in [5, 10, 15]:  # Prédictions à t+5s, t+10s, t+15s
            pred_x = x + vx * t
            pred_y = y + vy * t
            positions.append((pred_x, pred_y))
        
        return positions
    
    def _send_ssm(self, vehicle_id: str, granted: bool):
        """Envoi d'un Signal Status Message au véhicule"""
        status = "ACCORDÉE" if granted else "REFUSÉE"
        print(f"[V2I] SSM envoyé à {vehicle_id}: Priorité {status}")
    
    def _calculate_distance(self, position: tuple) -> float:
        """Calcul de distance entre véhicule et intersection"""
        # Simplifié: distance euclidienne
        x, y = position
        return ((x ** 2) + (y ** 2)) ** 0.5
    
    def resolve_conflict(self) -> Optional[str]:
        """
        Résolution des conflits de priorité selon le tableau de la section 3.2.3
        
        Returns:
            ID du véhicule ayant la priorité la plus élevée
        """
        if not self.active_requests:
            return None
        
        # Tri par niveau de priorité (P1 > P2 > P3)
        sorted_requests = sorted(
            self.active_requests.items(),
            key=lambda x: x[1].priority_level.value
        )
        
        winner_id, winner_msg = sorted_requests[0]
        
        if len(sorted_requests) > 1:
            print(f"\n[V2I] ⚠️  CONFLIT DE PRIORITÉ DÉTECTÉ")
            for vid, msg in sorted_requests:
                print(f"      - {vid}: {msg.priority_level.name}")
            print(f"      ✅ Résolution: {winner_id} ({winner_msg.priority_level.name})")
        
        return winner_id


# ============================================================================
# PARTIE 2: MODULE FAIL-SAFE
# ============================================================================

class OperatingMode(Enum):
    """Modes de fonctionnement selon section 3.2.3"""
    NORMAL = "Mode Normal (100% capacité)"
    DEGRADED_1 = "Mode Dégradé 1 (80% capacité)"
    DEGRADED_2 = "Mode Dégradé 2 (60% capacité)"
    SAFE_MODE = "Mode Sécurisé (Urgence)"


class FailureType(Enum):
    """Types de défaillances surveillées"""
    SUMO_COMMUNICATION_LOSS = "Perte communication SUMO"
    SENSOR_FAILURE = "Défaillance capteur"
    ALGORITHM_INCONSISTENCY = "Incohérence algorithme"
    POWER_FAILURE = "Coupure électrique"


@dataclass
class HealthMetrics:
    """Métriques de santé du système"""
    sumo_heartbeat: float  # Dernier heartbeat (timestamp)
    sensor_count: int  # Nombre de capteurs actifs
    controller_count: int  # Nombre de contrôleurs actifs
    latency_ms: float  # Latence système en ms
    power_voltage: float  # Tension électrique


class FailSafeModule:
    """Module de sûreté de fonctionnement (Fail-Safe)"""
    
    def __init__(self):
        self.current_mode = OperatingMode.NORMAL
        self.health_metrics = HealthMetrics(
            sumo_heartbeat=time.time(),
            sensor_count=4,  # 2 par voie (boucle + caméra)
            controller_count=3,  # Architecture TMR (Triple Modular Redundancy)
            latency_ms=30.0,
            power_voltage=220.0
        )
        
        # Seuils de détection selon tableau section 3.2.3
        self.HEARTBEAT_TIMEOUT = 3.0  # secondes
        self.MIN_SENSORS = 2
        self.MIN_CONTROLLERS = 2
        self.MAX_LATENCY_NORMAL = 50.0  # ms
        self.MAX_LATENCY_DEGRADED_1 = 100.0  # ms
        self.MIN_VOLTAGE = 200.0  # V
        
    def monitor_system(self) -> OperatingMode:
        """
        Surveillance continue du système et détection de défaillances
        
        Returns:
            Mode de fonctionnement actuel
        """
        failures = self._detect_failures()
        
        if failures:
            print(f"\n[FAIL-SAFE] ⚠️  DÉFAILLANCES DÉTECTÉES:")
            for failure in failures:
                print(f"             - {failure.value}")
            
            # Transition vers mode approprié
            new_mode = self._determine_mode(failures)
            
            if new_mode != self.current_mode:
                self._transition_mode(new_mode)
        
        return self.current_mode
    
    def _detect_failures(self) -> List[FailureType]:
        """Détection des défaillances selon les seuils définis"""
        failures = []
        
        # Check 1: Communication SUMO
        time_since_heartbeat = time.time() - self.health_metrics.sumo_heartbeat
        if time_since_heartbeat > self.HEARTBEAT_TIMEOUT:
            failures.append(FailureType.SUMO_COMMUNICATION_LOSS)
        
        # Check 2: Capteurs
        if self.health_metrics.sensor_count < self.MIN_SENSORS:
            failures.append(FailureType.SENSOR_FAILURE)
        
        # Check 3: Contrôleurs (TMR vote majoritaire)
        if self.health_metrics.controller_count < self.MIN_CONTROLLERS:
            failures.append(FailureType.ALGORITHM_INCONSISTENCY)
        
        # Check 4: Alimentation
        if self.health_metrics.power_voltage < self.MIN_VOLTAGE:
            failures.append(FailureType.POWER_FAILURE)
        
        return failures
    
    def _determine_mode(self, failures: List[FailureType]) -> OperatingMode:
        """
        Détermination du mode de fonctionnement selon les défaillances
        Implémente la machine d'états de la section 3.2.3
        """
        # Mode Sécurisé: défaillances critiques
        critical_failures = [
            FailureType.SUMO_COMMUNICATION_LOSS,
            FailureType.POWER_FAILURE,
            FailureType.ALGORITHM_INCONSISTENCY
        ]
        
        if any(f in failures for f in critical_failures):
            return OperatingMode.SAFE_MODE
        
        # Mode Dégradé 2: multiples capteurs défaillants
        if self.health_metrics.sensor_count <= 2:
            return OperatingMode.DEGRADED_2
        
        # Mode Dégradé 1: défaillance simple
        if len(failures) > 0 or self.health_metrics.latency_ms > self.MAX_LATENCY_NORMAL:
            return OperatingMode.DEGRADED_1
        
        # Mode Normal
        return OperatingMode.NORMAL
    
    def _transition_mode(self, new_mode: OperatingMode):
        """
        Transition entre modes de fonctionnement
        Selon procédures de la section 3.2.3
        """
        print(f"\n[FAIL-SAFE] 🔄 TRANSITION DE MODE")
        print(f"             Ancien: {self.current_mode.value}")
        print(f"             Nouveau: {new_mode.value}")
        
        # Actions spécifiques selon le nouveau mode
        if new_mode == OperatingMode.SAFE_MODE:
            self._activate_safe_mode()
        elif new_mode == OperatingMode.DEGRADED_2:
            self._activate_degraded_2()
        elif new_mode == OperatingMode.DEGRADED_1:
            self._activate_degraded_1()
        else:
            self._activate_normal_mode()
        
        self.current_mode = new_mode
        print(f"             ✅ Transition complétée")
    
    def _activate_safe_mode(self):
        """Activation du mode sécurisé (feux fixes conservatifs)"""
        print(f"[FAIL-SAFE] 🚨 MODE SÉCURISÉ ACTIVÉ")
        print(f"             - Feux fixes: 60s rouge / 30s vert")
        print(f"             - Notification opérateurs: ENVOYÉE")
        print(f"             - V2I: Mode manuel uniquement")
    
    def _activate_degraded_2(self):
        """Activation du mode dégradé 2 (plan semi-adaptatif)"""
        print(f"[FAIL-SAFE] ⚠️  MODE DÉGRADÉ 2 ACTIVÉ")
        print(f"             - Plan semi-adaptatif basé sur historique")
        print(f"             - V2I maintenu pour P1/P2")
    
    def _activate_degraded_1(self):
        """Activation du mode dégradé 1 (fusion de données)"""
        print(f"[FAIL-SAFE] ⚠️  MODE DÉGRADÉ 1 ACTIVÉ")
        print(f"             - Fusion données capteurs redondants")
        print(f"             - Latence augmentée: < 100ms")
    
    def _activate_normal_mode(self):
        """Retour au mode normal"""
        print(f"[FAIL-SAFE] ✅ RETOUR MODE NORMAL")
        print(f"             - Max-Pressure + V2I actifs")
        print(f"             - Latence: < 50ms")
    
    def inject_failure(self, failure_type: FailureType):
        """
        Injection de panne pour tests (simulation)
        Utilisé dans les tests unitaires de validation
        """
        print(f"\n[TEST] 💉 INJECTION DE PANNE: {failure_type.value}")
        
        if failure_type == FailureType.SUMO_COMMUNICATION_LOSS:
            self.health_metrics.sumo_heartbeat = time.time() - 10  # 10s ago
        elif failure_type == FailureType.SENSOR_FAILURE:
            self.health_metrics.sensor_count = 1
        elif failure_type == FailureType.ALGORITHM_INCONSISTENCY:
            self.health_metrics.controller_count = 1
        elif failure_type == FailureType.POWER_FAILURE:
            self.health_metrics.power_voltage = 150.0
    
    def restore_system(self):
        """Restauration du système après correction de panne"""
        print(f"\n[FAIL-SAFE] 🔧 RESTAURATION DU SYSTÈME")
        
        self.health_metrics.sumo_heartbeat = time.time()
        self.health_metrics.sensor_count = 4
        self.health_metrics.controller_count = 3
        self.health_metrics.latency_ms = 30.0
        self.health_metrics.power_voltage = 220.0
        
        print(f"             ✅ Tous les systèmes restaurés")


# ============================================================================
# PARTIE 3: INTÉGRATION V2I - FAIL-SAFE
# ============================================================================

class UrbanFlowSystem:
    """Système intégré Urban Flow avec V2I et Fail-Safe"""
    
    def __init__(self, intersection_id: str):
        self.v2i = V2IModule(intersection_id)
        self.failsafe = FailSafeModule()
        self.intersection_id = intersection_id
    
    def process_emergency_vehicle(self, vehicle_id: str, priority: VehicleType):
        """
        Traitement d'un véhicule d'urgence avec gestion Fail-Safe
        Démontre la synergie V2I - Fail-Safe (section C du rapport)
        """
        print(f"\n{'='*70}")
        print(f"TRAITEMENT VÉHICULE D'URGENCE: {vehicle_id}")
        print(f"{'='*70}")
        
        # 1. Vérifier l'état du système (Fail-Safe)
        current_mode = self.failsafe.monitor_system()
        print(f"\n[SYSTÈME] Mode actuel: {current_mode.value}")
        
        # 2. Créer et envoyer la requête V2I
        srm = V2IMessage(
            message_type=MessageType.SRM,
            vehicle_id=vehicle_id,
            timestamp=time.time(),
            position=(150, 100),  # Position exemple
            speed=15.0,  # 15 m/s ≈ 54 km/h
            priority_level=priority,
            eta=10.0,  # 10 secondes
            route=[self.intersection_id]
        )
        
        # 3. Traitement selon mode Fail-Safe
        if current_mode == OperatingMode.SAFE_MODE:
            print(f"[SYSTÈME] ⚠️  Mode Sécurisé actif")
            if priority == VehicleType.EMERGENCY_P1:
                print(f"[SYSTÈME] ✅ P1 maintenu même en mode sécurisé")
                self.v2i.receive_message(srm)
            else:
                print(f"[SYSTÈME] ❌ {priority.name} désactivé en mode sécurisé")
        else:
            # Mode normal ou dégradé: V2I opérationnel
            self.v2i.receive_message(srm)


# ============================================================================
# FONCTION DE DÉMONSTRATION
# ============================================================================

def demo_section_3_2_3():
    """
    Démonstration complète de la section 3.2.3
    À utiliser pour validation et présentation
    """
    print("\n" + "="*70)
    print("DÉMONSTRATION SECTION 3.2.3: INTÉGRATION V2I & FAIL-SAFE")
    print("Projet Urban Flow - ENIM 2025-2026")
    print("="*70)
    
    # Initialisation du système
    system = UrbanFlowSystem("Intersection_Agdal_Centre")
    
    # === SCÉNARIO 1: Fonctionnement normal ===
    print("\n\n[SCÉNARIO 1] FONCTIONNEMENT NORMAL")
    print("-" * 70)
    system.process_emergency_vehicle("AMB_001", VehicleType.EMERGENCY_P1)
    
    time.sleep(2)
    
    # === SCÉNARIO 2: Conflit de priorité ===
    print("\n\n[SCÉNARIO 2] CONFLIT DE PRIORITÉ")
    print("-" * 70)
    
    # Ambulance P1
    srm1 = V2IMessage(
        MessageType.SRM, "AMB_002", time.time(),
        (200, 150), 12.0, VehicleType.EMERGENCY_P1, 12.0
    )
    system.v2i.receive_message(srm1)
    
    # Police P2
    srm2 = V2IMessage(
        MessageType.SRM, "POL_001", time.time(),
        (180, 120), 14.0, VehicleType.EMERGENCY_P2, 10.0
    )
    system.v2i.receive_message(srm2)
    
    # Résolution
    winner = system.v2i.resolve_conflict()
    
    time.sleep(2)
    
    # === SCÉNARIO 3: Défaillance et mode dégradé ===
    print("\n\n[SCÉNARIO 3] DÉFAILLANCE CAPTEUR - MODE DÉGRADÉ")
    print("-" * 70)
    
    # Injection de panne
    system.failsafe.inject_failure(FailureType.SENSOR_FAILURE)
    
    # Traitement véhicule d'urgence en mode dégradé
    system.process_emergency_vehicle("FIRE_001", VehicleType.EMERGENCY_P1)
    
    time.sleep(2)
    
    # === SCÉNARIO 4: Mode sécurisé ===
    print("\n\n[SCÉNARIO 4] DÉFAILLANCE CRITIQUE - MODE SÉCURISÉ")
    print("-" * 70)
    
    # Injection de panne critique
    system.failsafe.inject_failure(FailureType.SUMO_COMMUNICATION_LOSS)
    
    # Tentative P2 (refusée)
    system.process_emergency_vehicle("POL_002", VehicleType.EMERGENCY_P2)
    
    # Tentative P1 (acceptée)
    system.process_emergency_vehicle("AMB_003", VehicleType.EMERGENCY_P1)
    
    time.sleep(2)
    
    # === SCÉNARIO 5: Restauration progressive ===
    print("\n\n[SCÉNARIO 5] RESTAURATION SYSTÈME")
    print("-" * 70)
    
    system.failsafe.restore_system()
    system.failsafe.monitor_system()
    
    print("\n" + "="*70)
    print("FIN DE LA DÉMONSTRATION")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Exécution de la démonstration
    demo_section_3_2_3()
    
    print("\n📝 Ce code illustre l'implémentation des concepts de la section 3.2.3")
    print("📊 Pour la validation complète, intégrer avec SUMO et Flask backend")
