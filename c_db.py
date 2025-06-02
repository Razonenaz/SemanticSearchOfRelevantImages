import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
from tqdm import tqdm

dataset_path = "dataset/caltech101/101_ObjectCategories/"
db_path = "my_vectordb"
collection_name = "caltech101_db"

chroma_client = chromadb.PersistentClient(path=db_path)
image_loader = ImageLoader()
multimodal_ef = OpenCLIPEmbeddingFunction()

try:
    chroma_client.delete_collection(name=collection_name)
    print(f"⚠️ Колекцію '{collection_name}' видалено перед створенням нової.")
except:
    print(f"ℹ️ Колекція '{collection_name}' не існувала або вже видалена.")

multimodal_db = chroma_client.create_collection(
    name=collection_name,
    embedding_function=multimodal_ef,
    data_loader=image_loader
)

image_paths = []
image_ids = []
metadatas = []

image_index = 0  

print("📊 Перевірка класів та підрахунок зображень:")

for class_name in tqdm(sorted(os.listdir(dataset_path)), desc="Індексація класів"):
    class_path = os.path.join(dataset_path, class_name)
    if not os.path.isdir(class_path):
        continue

    images_in_class = [
        img_file for img_file in os.listdir(class_path)
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ]

    print(f" - {class_name}: {len(images_in_class)} зображень")

    for img_file in images_in_class:
        full_path = os.path.join(class_path, img_file)

        image_paths.append(full_path.replace("\\", "/"))
        image_ids.append(f"{class_name}_{img_file}_{image_index}")
        metadatas.append({
            "class_name": class_name,
            "file_name": img_file
        })

        image_index += 1

batch_size = 100

for i in tqdm(range(0, len(image_paths), batch_size), desc="Додавання в базу"):
    try:
        multimodal_db.add(
            ids=image_ids[i:i+batch_size],
            uris=image_paths[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
    except Exception as e:
        print(f"❌ Помилка при додаванні batch {i}–{i+batch_size}: {e}")

print("✅ Базу даних ChromaDB створено і заповнено успішно!")
print(f"Кількість записів: {multimodal_db.count()}")