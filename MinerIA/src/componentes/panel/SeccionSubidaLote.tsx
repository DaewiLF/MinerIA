import { useRef } from "react";
import { Layers, Upload } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Button } from "../ui/Boton";
import { Heading } from "../ui/Encabezado";

interface BatchUploadSectionProps {
  batchFiles: File[];
  loading: boolean;
  result: string | null;
  onFilesChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onUpload: () => void;
}

export function BatchUploadSection({
  batchFiles,
  loading,
  result,
  onFilesChange,
  onUpload,
}: BatchUploadSectionProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Carga por lotes (Background)
        </Heading>
      </Card.Header>

      <Card.Body>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          multiple
          className="hidden"
          onChange={onFilesChange}
        />

        <div className="space-y-3">
          <Button
            variant="outline"
            onClick={() => inputRef.current?.click()}
            iconLeft={<Layers className="h-4 w-4" />}
            className="w-full"
          >
            {batchFiles.length > 0
              ? `${batchFiles.length} archivo(s) seleccionado(s)`
              : "Seleccionar imágenes"}
          </Button>

          <Button
            variant="primary"
            disabled={batchFiles.length === 0 || loading}
            onClick={onUpload}
            loading={loading}
            iconLeft={!loading ? <Upload className="h-4 w-4" /> : undefined}
            className="w-full"
          >
            {loading ? "Encolando..." : "Procesar lote en segundo plano"}
          </Button>

          {result && (
            <p className="text-small text-neutral-600">{result}</p>
          )}

          <p className="text-caption text-neutral-400">
            Las imágenes se procesarán secuencialmente sin bloquear la aplicación.
          </p>
        </div>
      </Card.Body>
    </Card>
  );
}
