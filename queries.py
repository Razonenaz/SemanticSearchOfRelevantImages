import traceback
import connect_to_db
import image_util

multimodal_db = connect_to_db.multimodal_db

def query_with_image(image_path: str, n_results: int = 9):
    query_image = image_util.prepare_image(image_path)

    query_results = multimodal_db.query(
        query_images=[query_image],
        n_results=n_results,
        include=['documents', 'distances', 'metadatas', 'data', 'uris']
    )
    return query_results

def query_with_text(query_text):
    
    if query_text:
        try:
            results = multimodal_db.query(
            query_texts=[query_text],
            n_results=9,
            include=['documents', 'distances', 'metadatas', 'data']
            )
            
            return results
        except Exception as e:
            traceback.print_exc()