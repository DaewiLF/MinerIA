import { useRef } from "react";
import { Video, Play } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Button } from "../ui/Boton";
import { Heading } from "../ui/Encabezado";

interface VideoUploadSectionProps {
  videoFile: File | null;
  loading: boolean;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onAnalyze: () => void;
}

export function VideoUploadSection({
  videoFile,
  loading,
  onFileChange,
  onAnalyze,
}: VideoUploadSectionProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <Card>
      <Card.Header>
        <Heading level={3} size="md">
          Cargar video (MP4 / MKV)
        </Heading>
      </Card.Header>

      <Card.Body>
        <input
          ref={inputRef}
          type="file"
          accept=".mp4,.mkv,video/*"
          className="hidden"
          onChange={onFileChange}
        />

        <div className="space-y-3">
          <Button
            variant="outline"
            onClick={() => inputRef.current?.click()}
            iconLeft={<Video className="h-4 w-4" />}
            className="w-full"
          >
            {videoFile ? "Cambiar video" : "Seleccionar video"}
          </Button>

          {videoFile && (
            <p className="text-small text-neutral-600 truncate">
              {videoFile.name}
            </p>
          )}

          <Button
            variant="primary"
            disabled={!videoFile || loading}
            onClick={onAnalyze}
            loading={loading}
            iconLeft={!loading ? <Play className="h-4 w-4" /> : undefined}
            className="w-full"
          >
            {loading ? "Analizando video..." : "Analizar video con IA"}
          </Button>

          <p className="text-caption text-neutral-400">
            Nota: MKV depende del codec del archivo.
          </p>
        </div>
      </Card.Body>
    </Card>
  );
}
