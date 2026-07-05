import exifr from "exifr";

export interface CoordenadasExtraidas {
  latitud: number;
  longitud: number;
  altitud?: number;
  fuente: "exif";
}

function formatearCoordenadas(lat: number, lon: number): string {
  const latDir = lat >= 0 ? "N" : "S";
  const lonDir = lon >= 0 ? "E" : "W";
  return `${Math.abs(lat).toFixed(6)}° ${latDir}, ${Math.abs(lon).toFixed(6)}° ${lonDir}`;
}

export async function extraerCoordenadasDeImagen(
  file: File
): Promise<{ coords: CoordenadasExtraidas; texto: string } | null> {
  try {
    const gps = await exifr.gps(file);
    if (!gps || gps.latitude == null || gps.longitude == null) return null;
    return {
      coords: {
        latitud: gps.latitude,
        longitud: gps.longitude,
        altitud: gps.altitude ?? undefined,
        fuente: "exif",
      },
      texto: formatearCoordenadas(gps.latitude, gps.longitude),
    };
  } catch {
    return null;
  }
}
