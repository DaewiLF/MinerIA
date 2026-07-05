import { Card } from "../ui/Tarjeta";
import { Input } from "../ui/Entrada";
import { Select } from "../ui/Seleccion";
import { Heading } from "../ui/Encabezado";

interface Metadata {
  category: string;
  riskLevel: string;
  location: string;
  coordinates: string;
  responsible: string;
  personnel: number;
}

interface MetaFormFieldsProps {
  modelId: string;
  modelOptions: { id: string; name: string }[];
  onModelChange: (id: string) => void;
  metadata: Metadata;
  onMetaChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
}

const categoryOptions = [
  { value: "Clasificación Mineral", label: "Clasificación Mineral" },
  { value: "Análisis de Tajo", label: "Análisis de Tajo" },
  { value: "Producción Activa", label: "Producción Activa" },
];

const riskOptions = [
  { value: "Bajo", label: "Bajo" },
  { value: "Medio", label: "Medio" },
  { value: "Alto", label: "Alto" },
];

export function MetaFormFields({
  modelId,
  modelOptions,
  onModelChange,
  metadata,
  onMetaChange,
}: MetaFormFieldsProps) {
  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Cargar imagen y metadatos
        </Heading>
      </Card.Header>

      <Card.Body>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Select
            label="Modelo IA"
            value={modelId}
            onChange={(e) => onModelChange(e.target.value)}
            options={modelOptions.map((m) => ({ value: m.id, label: m.name }))}
            selectSize="sm"
          />

          <Select
            label="Categoría"
            name="category"
            value={metadata.category}
            onChange={onMetaChange}
            options={categoryOptions}
            placeholder="Seleccionar"
            selectSize="sm"
          />

          <Select
            label="Nivel de riesgo"
            name="riskLevel"
            value={metadata.riskLevel}
            onChange={onMetaChange}
            options={riskOptions}
            placeholder="Seleccionar"
            selectSize="sm"
          />

          <Input
            label="Ubicación"
            name="location"
            value={metadata.location}
            onChange={onMetaChange}
            placeholder="Mina Norte - Zona A3"
            inputSize="sm"
          />

          <Input
            label="Coordenadas GPS"
            name="coordinates"
            value={metadata.coordinates}
            onChange={onMetaChange}
            placeholder={"23°45'12\"S 69°23'45\"W"}
            inputSize="sm"
          />

          <Input
            label="Responsable"
            name="responsible"
            value={metadata.responsible}
            onChange={onMetaChange}
            placeholder="Geólogo supervisor"
            inputSize="sm"
          />

          <Input
            label="Personal involucrado"
            name="personnel"
            type="number"
            value={metadata.personnel}
            onChange={onMetaChange}
            inputSize="sm"
            min={1}
          />
        </div>
      </Card.Body>
    </Card>
  );
}
