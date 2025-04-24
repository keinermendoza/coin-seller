export default function timeFormat(UTCDateTime, useSeconds=false) {
    const options = {
        // Formato de fecha
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        // Formato de hora
        hour: 'numeric',
        minute: 'numeric',
        // second: 'numeric',
        // Nombre o abreviatura de la zona horaria
        // timeZoneName: 'short',
        // Especificar la zona horaria deseada
        timeZone: 'America/Manaus'
      };

      if (useSeconds) options["second"] = "numeric";

      const date = new Date(UTCDateTime);
      
      // Convertir la fecha a una cadena en español, respetando la zona horaria especificada
      return date.toLocaleString('es-ES', options);
}