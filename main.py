
# Importar librerías
import pandas as pd
import streamlit as st
import xlsxwriter

from faker import Faker
from io import BytesIO


# Crear la clase principal en español
fake = Faker('es_ES')


# Características disponibles
caracteristicas_disponibles = {
    # Datos Personales
    "Nombre" : fake.name,
    "Dirección" : fake.street_address,
    "Email" : fake.email,
    "Teléfono" : fake.phone_number,
    "Fecha de nacimiento" : fake.date,
    "Dirección completa" : fake.address,
    "Códigos Postales" : fake.postcode,
    "Provincias" : fake.administrative_unit,
    "Comunidades Autónomas" : fake.autonomous_community,
    "Países" : fake.country,
    
    # Vehículos
    "Matrículas" : fake.license_plate_unified,
    "Bastidores" : fake.vin,
    
    # Banco
    "Números de Cuenta" : fake.bban,
    "IBAN" : fake.iban,  
    
    # Color
    "Colores" : fake.safe_color_name
}


# Características por defecto
caracteristicas_por_defecto = {
    "Nombre" : fake.name,
    "Fecha de nacimiento" : fake.date,
    "Dirección completa" : fake.address,
    "Teléfono" : fake.phone_number,
    "Email" : fake.email
}


# Función para generar los datos seleccionados
def generar_datos_fake(caracteristicas, num_rows):
    data = {field: [func() for _ in range(num_rows)] for field, func in caracteristicas.items()}
    return pd.DataFrame(data)


# Configuración de la disposición en columnas
col1, col2 = st.columns([1, 2])

# En la primera columna, colocamos la imagen
with col1:
    imagen_url = 'data_fake_logo.png'  # Reemplaza con la URL de tu imagen en línea
    st.image(imagen_url, width=210)

# En la segunda columna, colocamos el título
with col2:
    # Título y subtítulo
    st.title("Generador de datos - :red[FAKE]", anchor="3000")



# Desplegable para seleccionar campos
caracteristicas_seleccionadas = st.multiselect("Selecciona los campos",
                                               options=list(caracteristicas_disponibles.keys()),
                                               default=list(caracteristicas_por_defecto.keys()))
                                              


# Input de usuario para cantidad de datos
num_rows = st.number_input("Cantidad de datos a generar",
                           min_value=1,
                           max_value=10000,
                           value=1000)


# Condicional para generar datos. Si está presionado, se crean
if st.button("Generar datos", use_container_width=True):
    caracteristicas_func = {caracteristica : caracteristicas_disponibles[caracteristica] for caracteristica in caracteristicas_seleccionadas}
    df = generar_datos_fake(caracteristicas_func, num_rows)
    
    # Buffer donde se almacena el contenido, luego se borrará
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Reducir uso de memoria
        writer.book.use_constant_memory = True
        # Guardar archivo en excel
        df.to_excel(writer, index=False)
    # Mover puntero al inicio
    output.seek(0)
    
    st.success("Datos generados.")
    st.write(df)
        