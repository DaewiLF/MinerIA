import { useEffect, useState, useMemo } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Modal } from "./ui/Modal";
import { Button } from "./ui/Boton";
import { MapPin } from "lucide-react";

// Fix Leaflet default marker icon in bundlers
const defaultIcon = L.icon({
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});
L.Marker.prototype.options.icon = defaultIcon;

const DEFAULT_CENTER: [number, number] = [-23.5, -69.5];
const DEFAULT_ZOOM = 7;

function ClickHandler({
  onSelect,
}: {
  onSelect: (lat: number, lng: number) => void;
}) {
  useMapEvents({
    click(e) {
      onSelect(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function FlyTo({ center }: { center: [number, number] }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, Math.max(map.getZoom(), 13));
  }, [center, map]);
  return null;
}

interface MapaSelectorProps {
  abierto: boolean;
  onCerrar: () => void;
  onConfirmar: (texto: string) => void;
  inicial?: string;
}

function parseCoords(texto: string): [number, number] | null {
  const nums = texto
    .replace(/[°NSWE]/g, "")
    .split(/[,\s]+/)
    .map(Number)
    .filter((n) => !isNaN(n));
  if (nums.length >= 2) return [nums[0], nums[1]];
  return null;
}

export function MapaSelector({
  abierto,
  onCerrar,
  onConfirmar,
  inicial,
}: MapaSelectorProps) {
  const initialCoords = useMemo(() => parseCoords(inicial ?? ""), [inicial]);
  const [seleccion, setSeleccion] = useState<[number, number] | null>(
    initialCoords ?? null
  );
  const center: [number, number] = initialCoords ?? DEFAULT_CENTER;

  useEffect(() => {
    if (abierto) setSeleccion(initialCoords ?? null);
  }, [abierto, initialCoords]);

  const textoPreview = seleccion
    ? `${seleccion[0].toFixed(6)}, ${seleccion[1].toFixed(6)}`
    : "";

  return (
    <Modal open={abierto} onClose={onCerrar} title="Seleccionar ubicación" size="xl">
      <div className="space-y-4">
        <div className="h-[400px] rounded-lg overflow-hidden border border-neutral-200">
          <MapContainer
            center={center}
            zoom={DEFAULT_ZOOM}
            className="h-full w-full"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <ClickHandler
              onSelect={(lat, lng) => setSeleccion([lat, lng])}
            />
            {seleccion && (
              <>
                <Marker position={seleccion} />
                <FlyTo center={seleccion} />
              </>
            )}
          </MapContainer>
        </div>

        {seleccion && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-primary-50 text-primary-700 text-small">
            <MapPin className="h-4 w-4 shrink-0" />
            <span className="font-medium">{textoPreview}</span>
          </div>
        )}

        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={onCerrar}>
            Cancelar
          </Button>
          <Button
            disabled={!seleccion}
            onClick={() => {
              if (textoPreview) onConfirmar(textoPreview);
              onCerrar();
            }}
          >
            Confirmar ubicación
          </Button>
        </div>
      </div>
    </Modal>
  );
}
