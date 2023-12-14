import requests

def delete_post(post_id):


    url = "https://coinstrategdev.wpenginepowered.com/?wpwhpro_action=get_news&wpwhpro_api_key=5fjtogfdmtjbdljfnvmqt2och2fl3ppvjd9nkxdoa0jt1vkp9ri81nwm1lbfgfrn&action=delete_post"

    headers = {
        "Accept": "*/*",
        "User-Agent": "news",
    }

    json_payload = {
        "post_id": post_id
    }

    try:
        response = requests.post(url, headers=headers, json=json_payload)
        response.raise_for_status() 
        data = response.json()

        success = data.get("success", False)
        msg = data.get("msg", "")

        if success:
            post_id_deleted = data.get("data", {}).get("post_id", "")
            permalink = data.get("data", {}).get("permalink", "")


            return {
                "success": success,
                "msg": msg,
                "post_id_deleted": post_id_deleted,
                "permalink": permalink,
            }, 200
        
        else:
            return {
                "success": success,
                "msg": msg
            }, 400
        
    except requests.exceptions.RequestException as e:
        print(f"Error deleting post_id: {post_id}, response: {e}")
        return {"success": False, "msg": str(e)}, 500

# Example usage
post_id_to_delete = 57
result = delete_post(post_id_to_delete)

print(result)
