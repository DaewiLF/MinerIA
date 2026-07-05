import { Link } from "react-router-dom";
import { Pickaxe, Home } from "lucide-react";
import { Button } from "../componentes/ui/Boton";

export function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50">
      <div className="text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-primary-50 flex items-center justify-center mx-auto">
          <Pickaxe className="h-8 w-8 text-primary-600" />
        </div>
        <h1 className="text-heading-xl text-neutral-800">404</h1>
        <p className="text-body text-neutral-500 max-w-sm">
          La página que buscas no existe o ha sido movida.
        </p>
        <Link to="/dashboard">
          <Button variant="primary" iconLeft={<Home className="h-4 w-4" />}>
            Volver al inicio
          </Button>
        </Link>
      </div>
    </div>
  );
}
