import { useRef } from "react";
import { Upload, Image as ImageIcon, RotateCcw } from "lucide-react";
import { Card } from "../ui/Tarjeta";
import { Button } from "../ui/Boton";

interface ImageUploadSectionProps {
  filePreview: string | null;
  loading: boolean;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onAnalyze: () => void;
}

export function ImageUploadSection({
  filePreview,
  loading,
  onFileChange,
  onAnalyze,
}: ImageUploadSectionProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <Card>
      <Card.Body>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={onFileChange}
        />

        {!filePreview ? (
          <div
            onClick={() => inputRef.current?.click()}
            className="border-2 border-dashed border-neutral-300 rounded-xl p-10 text-center cursor-pointer hover:border-primary-400 hover:bg-primary-50/30 transition-all duration-fast"
          >
            <div className="mb-3 text-neutral-300">
              <Upload className="h-10 w-10 mx-auto" />
            </div>
            <p className="text-body-bold text-neutral-700 mb-1">
              Arrastra una imagen aquí
            </p>
            <p className="text-small text-neutral-400">o haz clic para seleccionar</p>
            <p className="text-caption text-neutral-400 mt-3">
              Formatos soportados: JPG, PNG
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <img
              src={filePreview}
              alt="Imagen subida"
              className="w-full rounded-xl border border-neutral-200 max-h-80 object-contain bg-neutral-50"
            />

            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => inputRef.current?.click()}
                iconLeft={<RotateCcw className="h-4 w-4" />}
                className="flex-1"
              >
                Cambiar imagen
              </Button>

              <Button
                variant="primary"
                onClick={onAnalyze}
                loading={loading}
                iconLeft={!loading ? <ImageIcon className="h-4 w-4" /> : undefined}
                className="flex-1"
              >
                {loading ? "Analizando..." : "Analizar con IA"}
              </Button>
            </div>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
