import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const icon = L.icon({
  iconUrl: '/images/marker-icon.png',
  iconRetinaUrl: '/images/marker-icon-2x.png',
  shadowUrl: '/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

type Props = {
    vessels: {
        mmsi: number;
        lat: number;
        lon: number;
        sog: number;
        cog: number;
    }[];
};

const MapView = ({ vessels }: Props) => {
    return (
        <MapContainer center={[60.1699, 24.9384]} zoom={6} scrollWheelZoom style={{ height: '500px', width: '100%' }}>
            <TileLayer
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {vessels.map((v) => (
                <Marker 
                    key={v.mmsi} 
                    position={[v.lat, v.lon]}
                    icon={icon}
                >
                    <Popup>
                        <strong>MMSI:</strong> {v.mmsi}<br />
                        <strong>SOG:</strong> {v.sog} kn<br />
                        <strong>COG:</strong> {v.cog}°
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
};

export default MapView;
