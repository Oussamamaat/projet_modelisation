/**
 * V2I Dashboard Interface - Urban Flow
 * Module de supervision des véhicules d'urgence
 * 
 * Section 3.3.3 - ENIM 2025-2026
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Circle, Polyline, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// ============================================================================
// TYPES ET INTERFACES
// ============================================================================

const VehicleType = {
  AMBULANCE: 'ambulance',
  FIRE: 'fire',
  POLICE: 'police'
};

const PriorityLevel = {
  P1: { level: 1, label: 'P1 - Critique', color: '#C41E3A', bgColor: '#FFE5E8' },
  P2: { level: 2, label: 'P2 - Haute', color: '#FF9800', bgColor: '#FFF3E0' },
  P3: { level: 3, label: 'P3 - Standard', color: '#FFC107', bgColor: '#FFFDE7' }
};

const RequestStatus = {
  PENDING: 'En attente',
  GRANTED: 'Accordée',
  ACTIVE: 'En cours',
  COMPLETED: 'Terminée'
};

const AlertLevel = {
  CRITICAL: { level: 'critical', color: '#C41E3A', sound: true },
  WARNING: { level: 'warning', color: '#FF9800', sound: false },
  INFO: { level: 'info', color: '#2196F3', sound: false }
};

// ============================================================================
// ICÔNES PERSONNALISÉES POUR LES VÉHICULES
// ============================================================================

const createVehicleIcon = (type, priority) => {
  const icons = {
    ambulance: '🚑',
    fire: '🚒',
    police: '🚓'
  };
  
  const color = PriorityLevel[priority]?.color || '#666';
  
  return L.divIcon({
    html: `
      <div style="
        position: relative;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <div style="
          position: absolute;
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background: ${color};
          opacity: 0.3;
          animation: pulse 2s infinite;
        "></div>
        <div style="
          font-size: 24px;
          z-index: 10;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        ">${icons[type] || '🚗'}</div>
      </div>
      <style>
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 0.3; }
          50% { transform: scale(1.5); opacity: 0.1; }
        }
      </style>
    `,
    className: 'vehicle-marker',
    iconSize: [40, 40],
    iconAnchor: [20, 20]
  });
};

// ============================================================================
// COMPOSANT: CARTE INTERACTIVE
// ============================================================================

const EmergencyVehicleMap = ({ vehicles, trafficLights, corridors }) => {
  const center = [33.9716, -6.8498]; // Rabat, Morocco
  const zoom = 14;

  return (
    <div style={{ height: '600px', width: '100%', borderRadius: '8px', overflow: 'hidden' }}>
      <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        
        {/* Zones de détection V2I (RSU) */}
        {trafficLights.map(light => (
          <Circle
            key={`rsu-${light.id}`}
            center={[light.position.lat, light.position.lng]}
            radius={300}
            pathOptions={{
              color: '#2E5C8A',
              fillColor: '#2E5C8A',
              fillOpacity: 0.1,
              weight: 1,
              dashArray: '5, 5'
            }}
          />
        ))}

        {/* Feux tricolores */}
        {trafficLights.map(light => (
          <Marker
            key={light.id}
            position={[light.position.lat, light.position.lng]}
            icon={L.divIcon({
              html: `
                <div style="
                  width: 20px;
                  height: 20px;
                  border-radius: 50%;
                  background: ${light.state === 'green' ? '#4CAF50' : light.state === 'yellow' ? '#FFC107' : '#C41E3A'};
                  border: ${light.priorityMode ? '3px solid #2E5C8A' : '2px solid #666'};
                  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                "></div>
              `,
              className: 'traffic-light-marker',
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            })}
          >
            <Popup>
              <div style={{ padding: '8px' }}>
                <strong>{light.id}</strong><br/>
                État: {light.state === 'green' ? 'Vert 🟢' : light.state === 'yellow' ? 'Jaune 🟡' : 'Rouge 🔴'}<br/>
                {light.priorityMode && <span style={{ color: '#2E5C8A', fontWeight: 'bold' }}>Mode Priorité Actif</span>}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Corridors de vague verte */}
        {corridors.map(corridor => (
          <Polyline
            key={corridor.id}
            positions={corridor.path}
            pathOptions={{
              color: '#4CAF50',
              weight: 8,
              opacity: 0.6,
              dashArray: '10, 5'
            }}
          />
        ))}

        {/* Véhicules d'urgence */}
        {vehicles.map(vehicle => (
          <React.Fragment key={vehicle.id}>
            {/* Marqueur du véhicule */}
            <Marker
              position={[vehicle.position.lat, vehicle.position.lng]}
              icon={createVehicleIcon(vehicle.type, vehicle.priority)}
            >
              <Popup>
                <div style={{ padding: '8px' }}>
                  <strong>{vehicle.id}</strong><br/>
                  Type: {vehicle.type}<br/>
                  Priorité: <span style={{
                    background: PriorityLevel[vehicle.priority]?.bgColor,
                    color: PriorityLevel[vehicle.priority]?.color,
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontWeight: 'bold'
                  }}>
                    {vehicle.priority}
                  </span><br/>
                  Vitesse: {vehicle.speed.toFixed(1)} m/s<br/>
                  ETA: {vehicle.eta}s<br/>
                  Statut: {vehicle.status}
                </div>
              </Popup>
            </Marker>

            {/* Trajectoire prédite */}
            {vehicle.predictedPath && (
              <Polyline
                positions={vehicle.predictedPath}
                pathOptions={{
                  color: '#2196F3',
                  weight: 2,
                  opacity: 0.5,
                  dashArray: '5, 10'
                }}
              />
            )}
          </React.Fragment>
        ))}
      </MapContainer>
    </div>
  );
};

// ============================================================================
// COMPOSANT: PANNEAU DES REQUÊTES ACTIVES
// ============================================================================

const ActiveRequestsPanel = ({ requests, onManualControl }) => {
  const [sortBy, setSortBy] = useState('priority'); // 'priority' | 'eta' | 'time'
  const [filterPriority, setFilterPriority] = useState('all');

  const sortedRequests = useMemo(() => {
    let filtered = requests;
    
    if (filterPriority !== 'all') {
      filtered = requests.filter(r => r.priority === filterPriority);
    }

    return [...filtered].sort((a, b) => {
      if (sortBy === 'priority') {
        return PriorityLevel[a.priority].level - PriorityLevel[b.priority].level;
      } else if (sortBy === 'eta') {
        return a.eta - b.eta;
      } else {
        return new Date(a.timestamp) - new Date(b.timestamp);
      }
    });
  }, [requests, sortBy, filterPriority]);

  return (
    <div style={{
      background: 'white',
      borderRadius: '8px',
      padding: '20px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      height: '600px',
      overflowY: 'auto'
    }}>
      <h3 style={{ marginTop: 0, color: '#2E5C8A' }}>
        Requêtes Actives ({requests.length})
      </h3>

      {/* Filtres et tri */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{
            padding: '8px 12px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '14px'
          }}
        >
          <option value="priority">Trier par Priorité</option>
          <option value="eta">Trier par ETA</option>
          <option value="time">Trier par Heure</option>
        </select>

        <select
          value={filterPriority}
          onChange={(e) => setFilterPriority(e.target.value)}
          style={{
            padding: '8px 12px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '14px'
          }}
        >
          <option value="all">Toutes les priorités</option>
          <option value="P1">P1 uniquement</option>
          <option value="P2">P2 uniquement</option>
          <option value="P3">P3 uniquement</option>
        </select>
      </div>

      {/* Liste des requêtes */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {sortedRequests.map(request => (
          <RequestCard
            key={request.id}
            request={request}
            onManualControl={onManualControl}
          />
        ))}

        {sortedRequests.length === 0 && (
          <div style={{
            textAlign: 'center',
            padding: '40px',
            color: '#999',
            fontSize: '14px'
          }}>
            Aucune requête active
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// COMPOSANT: CARTE DE REQUÊTE
// ============================================================================

const RequestCard = ({ request, onManualControl }) => {
  const priority = PriorityLevel[request.priority];
  const vehicleIcons = {
    ambulance: '🚑',
    fire: '🚒',
    police: '🚓'
  };

  return (
    <div style={{
      border: `2px solid ${priority.color}`,
      borderRadius: '8px',
      padding: '15px',
      background: priority.bgColor,
      transition: 'transform 0.2s',
      cursor: 'pointer'
    }}
    onMouseEnter={(e) => e.currentTarget.style.transform = 'translateX(5px)'}
    onMouseLeave={(e) => e.currentTarget.style.transform = 'translateX(0)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <span style={{ fontSize: '24px' }}>{vehicleIcons[request.type]}</span>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{request.id}</div>
              <div style={{
                background: priority.color,
                color: 'white',
                padding: '2px 8px',
                borderRadius: '12px',
                fontSize: '12px',
                display: 'inline-block',
                fontWeight: 'bold'
              }}>
                {priority.label}
              </div>
            </div>
          </div>

          <div style={{ fontSize: '14px', color: '#555', lineHeight: '1.6' }}>
            <div>⏱️ ETA: <strong>{request.eta}s</strong></div>
            <div>📍 Distance: <strong>{request.distance}m</strong></div>
            <div>📊 Statut: <strong>{request.status}</strong></div>
            <div style={{ fontSize: '12px', color: '#888', marginTop: '4px' }}>
              Reçu: {new Date(request.timestamp).toLocaleTimeString('fr-FR')}
            </div>
          </div>
        </div>

        {/* Boutons d'action */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <button
            onClick={() => onManualControl(request.id, 'force')}
            style={{
              padding: '6px 12px',
              background: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '12px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
            title="Forcer l'activation"
          >
            ✓ Forcer
          </button>
          <button
            onClick={() => onManualControl(request.id, 'suspend')}
            style={{
              padding: '6px 12px',
              background: '#FF9800',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '12px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
            title="Suspendre temporairement"
          >
            ⏸ Suspendre
          </button>
          <button
            onClick={() => onManualControl(request.id, 'cancel')}
            style={{
              padding: '6px 12px',
              background: '#C41E3A',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '12px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
            title="Annuler définitivement"
          >
            ✕ Annuler
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// COMPOSANT: BARRE DE MÉTRIQUES
// ============================================================================

const MetricsBar = ({ metrics }) => {
  const metricCards = [
    {
      label: 'Requêtes Actives',
      value: metrics.activeRequests,
      threshold: 5,
      unit: '',
      icon: '📊'
    },
    {
      label: 'Temps Moyen',
      value: metrics.avgTime,
      threshold: 60,
      unit: 's',
      icon: '⏱️'
    },
    {
      label: 'Taux de Succès',
      value: metrics.successRate,
      threshold: 95,
      unit: '%',
      icon: '✓',
      inverted: true // Higher is better
    },
    {
      label: 'Latence',
      value: metrics.latency,
      threshold: 200,
      unit: 'ms',
      icon: '⚡'
    }
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '15px',
      padding: '20px',
      background: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
    }}>
      {metricCards.map((metric, idx) => {
        const isAlert = metric.inverted 
          ? metric.value < metric.threshold 
          : metric.value > metric.threshold;
        
        return (
          <div
            key={idx}
            style={{
              padding: '15px',
              background: isAlert ? '#FFE5E8' : '#F5F5F5',
              borderRadius: '8px',
              border: isAlert ? '2px solid #C41E3A' : '2px solid transparent'
            }}
          >
            <div style={{ fontSize: '24px', marginBottom: '8px' }}>{metric.icon}</div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
              {metric.label}
            </div>
            <div style={{
              fontSize: '28px',
              fontWeight: 'bold',
              color: isAlert ? '#C41E3A' : '#2E5C8A'
            }}>
              {metric.value}{metric.unit}
            </div>
            {isAlert && (
              <div style={{ fontSize: '11px', color: '#C41E3A', marginTop: '4px' }}>
                ⚠️ Seuil dépassé
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

// ============================================================================
// COMPOSANT: SYSTÈME D'ALERTES
// ============================================================================

const AlertsManager = ({ alerts, onDismiss }) => {
  return (
    <div style={{
      position: 'fixed',
      top: '20px',
      right: '20px',
      zIndex: 10000,
      display: 'flex',
      flexDirection: 'column',
      gap: '10px',
      maxWidth: '400px'
    }}>
      {alerts.map(alert => (
        <div
          key={alert.id}
          style={{
            background: 'white',
            borderLeft: `4px solid ${AlertLevel[alert.level].color}`,
            borderRadius: '8px',
            padding: '15px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            animation: 'slideIn 0.3s ease-out'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ flex: 1 }}>
              <div style={{
                fontWeight: 'bold',
                color: AlertLevel[alert.level].color,
                marginBottom: '8px',
                fontSize: '14px'
              }}>
                {alert.level === 'CRITICAL' && '🚨 ALERTE CRITIQUE'}
                {alert.level === 'WARNING' && '⚠️ AVERTISSEMENT'}
                {alert.level === 'INFO' && 'ℹ️ INFORMATION'}
              </div>
              <div style={{ fontSize: '13px', color: '#555' }}>
                {alert.message}
              </div>
              <div style={{ fontSize: '11px', color: '#999', marginTop: '6px' }}>
                {new Date(alert.timestamp).toLocaleTimeString('fr-FR')}
              </div>
            </div>
            <button
              onClick={() => onDismiss(alert.id)}
              style={{
                background: 'transparent',
                border: 'none',
                fontSize: '18px',
                cursor: 'pointer',
                color: '#999',
                marginLeft: '10px'
              }}
            >
              ✕
            </button>
          </div>
        </div>
      ))}
      <style>{`
        @keyframes slideIn {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};

// ============================================================================
// COMPOSANT PRINCIPAL: TABLEAU DE BORD V2I
// ============================================================================

const V2IDashboard = () => {
  const [vehicles, setVehicles] = useState([]);
  const [trafficLights, setTrafficLights] = useState([]);
  const [corridors, setCorridors] = useState([]);
  const [activeRequests, setActiveRequests] = useState([]);
  const [metrics, setMetrics] = useState({
    activeRequests: 0,
    avgTime: 0,
    successRate: 100,
    latency: 45
  });
  const [alerts, setAlerts] = useState([]);
  const [websocket, setWebsocket] = useState(null);

  // Connexion WebSocket au backend
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:5000/v2i');
    
    ws.onopen = () => {
      console.log('[V2I] WebSocket connecté');
      addAlert('INFO', 'Connexion établie avec le serveur V2I');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleWebSocketMessage(message);
    };

    ws.onerror = (error) => {
      console.error('[V2I] Erreur WebSocket:', error);
      addAlert('CRITICAL', 'Erreur de connexion WebSocket');
    };

    ws.onclose = () => {
      console.log('[V2I] WebSocket déconnecté');
      addAlert('WARNING', 'Connexion au serveur V2I perdue');
    };

    setWebsocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  // Gestion des messages WebSocket
  const handleWebSocketMessage = (message) => {
    switch (message.type) {
      case 'vehicle_update':
        updateVehicle(message.data);
        break;
      case 'priority_granted':
        handlePriorityGranted(message.data);
        break;
      case 'traffic_light_state':
        updateTrafficLight(message.data);
        break;
      case 'metrics_update':
        setMetrics(message.data);
        break;
      default:
        console.warn('[V2I] Message non reconnu:', message.type);
    }
  };

  // Mise à jour des véhicules
  const updateVehicle = (vehicleData) => {
    setVehicles(prev => {
      const index = prev.findIndex(v => v.id === vehicleData.id);
      if (index >= 0) {
        const updated = [...prev];
        updated[index] = { ...updated[index], ...vehicleData };
        return updated;
      }
      return [...prev, vehicleData];
    });

    // Mise à jour des requêtes actives
    if (vehicleData.requestActive) {
      setActiveRequests(prev => {
        const index = prev.findIndex(r => r.id === vehicleData.id);
        if (index >= 0) {
          const updated = [...prev];
          updated[index] = {
            ...updated[index],
            ...vehicleData,
            timestamp: vehicleData.timestamp || updated[index].timestamp
          };
          return updated;
        }
        return [...prev, {
          id: vehicleData.id,
          type: vehicleData.type,
          priority: vehicleData.priority,
          eta: vehicleData.eta,
          distance: vehicleData.distance,
          status: vehicleData.status,
          timestamp: Date.now()
        }];
      });
    }
  };

  // Gestion de l'accordement de priorité
  const handlePriorityGranted = (data) => {
    addAlert('INFO', `Vague verte accordée pour ${data.vehicle_id}`);
    setCorridors(prev => [...prev, data.corridor]);
  };

  // Mise à jour des feux
  const updateTrafficLight = (lightData) => {
    setTrafficLights(prev => {
      const index = prev.findIndex(l => l.id === lightData.intersection_id);
      if (index >= 0) {
        const updated = [...prev];
        updated[index] = {
          ...updated[index],
          state: lightData.state,
          timeRemaining: lightData.time_remaining
        };
        return updated;
      }
      return prev;
    });
  };

  // Ajout d'alerte
  const addAlert = (level, message) => {
    const alert = {
      id: Date.now(),
      level,
      message,
      timestamp: Date.now()
    };
    
    setAlerts(prev => [...prev, alert]);

    // Alerte sonore pour niveaux critiques
    if (AlertLevel[level].sound) {
      // Jouer un son d'alerte (implémentation dépendante du navigateur)
      console.log('🔊 ALERTE SONORE:', message);
    }

    // Auto-dismiss après 10 secondes (sauf critiques)
    if (level !== 'CRITICAL') {
      setTimeout(() => {
        dismissAlert(alert.id);
      }, 10000);
    }
  };

  // Suppression d'alerte
  const dismissAlert = (alertId) => {
    setAlerts(prev => prev.filter(a => a.id !== alertId));
  };

  // Contrôle manuel
  const handleManualControl = (vehicleId, action) => {
    const confirmActions = {
      force: 'Êtes-vous sûr de vouloir forcer l\'activation de la priorité ?',
      suspend: 'Êtes-vous sûr de vouloir suspendre cette requête ?',
      cancel: 'Êtes-vous sûr de vouloir annuler définitivement cette requête ?'
    };

    if (window.confirm(confirmActions[action])) {
      // Envoyer au backend
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({
          type: 'manual_control',
          vehicle_id: vehicleId,
          action: action,
          operator_id: 'operator_001', // Remplacer par ID réel
          timestamp: Date.now()
        }));

        addAlert('INFO', `Action "${action}" exécutée pour ${vehicleId}`);
      } else {
        addAlert('CRITICAL', 'Impossible d\'envoyer la commande - WebSocket déconnecté');
      }
    }
  };

  return (
    <div style={{
      background: '#F5F7FA',
      minHeight: '100vh',
      padding: '20px'
    }}>
      {/* En-tête */}
      <div style={{
        background: 'white',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '20px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{
          margin: 0,
          color: '#2E5C8A',
          fontSize: '28px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          🚨 Module V2I - Supervision Véhicules d'Urgence
        </h1>
        <div style={{ fontSize: '14px', color: '#666', marginTop: '8px' }}>
          Urban Flow - Centre de Gestion du Trafic
        </div>
      </div>

      {/* Alertes */}
      <AlertsManager alerts={alerts} onDismiss={dismissAlert} />

      {/* Grille principale */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 400px',
        gap: '20px',
        marginBottom: '20px'
      }}>
        {/* Carte */}
        <div>
          <EmergencyVehicleMap
            vehicles={vehicles}
            trafficLights={trafficLights}
            corridors={corridors}
          />
        </div>

        {/* Panneau des requêtes */}
        <div>
          <ActiveRequestsPanel
            requests={activeRequests}
            onManualControl={handleManualControl}
          />
        </div>
      </div>

      {/* Barre de métriques */}
      <MetricsBar metrics={metrics} />
    </div>
  );
};

export default V2IDashboard;
