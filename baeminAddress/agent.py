import requests
from google.adk.agents import Agent

def search_restaurant(keyword: str) -> dict:
    """Searches for restaurants using Kakao API.

    Args:
        keyword (str): The restaurant name or keyword to search for.

    Returns:
        dict: status and result or error msg.
    """
    print(f"DEBUG: search_restaurant called with keyword={keyword}")
    api_key = "0c6a22f38fa661f0fc9384f35e136c54"  # 카카오 API 키
    
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    
    params = {
        "query": keyword,
        "category_group_code": "FD6",  # FD6: 음식점 카테고리
        "size": 15
    }
    
    try:
        print(f"DEBUG: Making request to Kakao API")
        response = requests.get(url, headers=headers, params=params)
        print(f"DEBUG: Kakao API response status code: {response.status_code}")
        
        data = response.json()
        
        if data.get("documents"):
            results = []
            total_count = data["meta"]["total_count"]
            print(f"DEBUG: Found {total_count} total results, {len(data['documents'])} documents")
            
            for place in data["documents"]:
                if len(data["documents"]) > 1:
                    # Return only name and address when there are multiple results
                    result = {
                        "name": place['place_name'],
                        "address": place['address_name']
                    }
                else:
                    # Return full details when there's only one result
                    result = {
                        "name": place['place_name'],
                        "address": place['address_name'],
                        "road_address": place['road_address_name'],
                        "category": place['category_name'],
                        "phone": place['phone'],
                        "location": {
                            "latitude": place['y'],
                            "longitude": place['x']
                        }
                    }
                results.append(result)
            
            # If there's only one result, automatically call search_baemin
            if len(results) == 1 and len(data["documents"]) == 1:
                print(f"DEBUG: Single result found. Calling search_baemin for {results[0]['name']}")
                print(f"DEBUG: Coordinates - lat: {results[0]['location']['latitude']}, lng: {results[0]['location']['longitude']}")
                
                # Ensure location data is available
                if 'location' in results[0] and 'latitude' in results[0]['location'] and 'longitude' in results[0]['location']:
                    baemin_result = search_baemin(
                        name=results[0]['name'],
                        latitude=results[0]['location']['latitude'],
                        longitude=results[0]['location']['longitude']
                    )
                    
                    print(f"DEBUG: Baemin API response status: {baemin_result.get('status')}")
                    
                    # Add Baemin data to the response
                    return {
                        "status": "success",
                        "results": results,
                        "total_count": total_count,
                        "baemin_data": baemin_result
                    }
                else:
                    print(f"DEBUG: Missing location data in result")
                    return {
                        "status": "success",
                        "results": results,
                        "total_count": total_count,
                        "error_message": "Missing location data for Baemin search"
                    }
            else:
                print(f"DEBUG: Multiple results found ({len(results)}). Not calling search_baemin.")
                return {
                    "status": "success",
                    "results": results,
                    "total_count": total_count
                }
        else:
            print(f"DEBUG: No results found for '{keyword}'")
            return {
                "status": "error",
                "error_message": f"'{keyword}' 검색 결과가 없습니다."
            }
            
    except Exception as e:
        print(f"DEBUG: Exception in search_restaurant: {str(e)}")
        return {
            "status": "error",
            "error_message": f"검색 중 오류가 발생했습니다: {str(e)}"
        }

def search_baemin(name: str, latitude: str, longitude: str) -> dict:
    """Searches for restaurant information in Baemin using the name and coordinates.
    
    Args:
        name (str): The restaurant name to search for.
        latitude (str): The latitude coordinate.
        longitude (str): The longitude coordinate.
        
    Returns:
        dict: Baemin search results or error message.
    """
    print(f"DEBUG: search_baemin called with name={name}, lat={latitude}, lng={longitude}")
    url = "https://search-gateway.baemin.com/v1/search"
    
    # Convert latitude and longitude to string if they are not already
    lat = str(latitude) if not isinstance(latitude, str) else latitude
    lng = str(longitude) if not isinstance(longitude, str) else longitude
    
    headers = {
        "Authorization": "bearer guest",
        "User-Agent": "and1_15.3.2",
        "Carrier": "45005",
        "Device-Height": "1280",
        "Device-Width": "720",
        "USER-BAEDAL": "1VXD9fUH1bpOE6lhKdZKOQ834NBMSOlqem045YFcadVazzICLf606VgmIM6IykqbYCt+z/lhKfgW8NV31aNUaWJqVDUtY3Nb29je7jdZpeRm1TPKUNNikWe9MS7R088AVPgmK4dsHaWgPsbiM4KhZR28WhQDJ0/aE5I553CbK6o7fb/KwXT99Vw9UhD/Dllz",
        "Host": "search-gateway.baemin.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    params = {
        "keyword": name,
        "currentTab": "ALL",
        "offset": "0",
        "referral": "Search",
        "entryPoint": "",
        "searchHomeType": "FOOD",
        "kind": "DEFAULT",
        "limit": "25",
        "latitude": lat,
        "longitude": lng,
        "isFirstRequest": "true",
        "extension": "",
        "baeminDeliveryFilter": "",
        "baeminDeliverySort": "",
        "baeminTakeoutFilter": "",
        "baeminTakeoutSort": "",
        "isBmartRegion": "false",
        "isBaeminStoreRegion": "true",
        "commerceSort": "",
        "commerceCursor": "",
        "commerceFilters": "",
        "commerceSelectedSellerId": "",
        "commerceSelectedShopId": "",
        "commerceSearchType": "DEFAULT",
        "hyperMarketSort": "",
        "hyperMarketSearchType": "DEFAULT",
        "perseusSessionId": "1746756991224.116893199435289199.mSmwpJzDCI",
        "memberNumber": "000000000000",
        "commerceLastWinnerCategoryId": "",
        "sessionId": "eb664672f5466d2b44257294e",
        "carrier": "45005",
        "site": "7jWXRELC2e",
        "dvcid": "OPUDbaa0c2d3c4480d69",
        "adid": "d89e7f78-631c-48ad-91b1-396c63874c87",
        "deviceModel": "SM-G988N",
        "appver": "15.3.2",
        "oscd": "2",
        "osver": "28",
        "dongCode": "42130112",
        "zipCode": "26316",
        "perseusClientId": "1733450321960.935983848749139217.N1U1OYWFJ5",
        "actionTrackingKey": "4557"
    }
    
    try:
        # Use SSL verification but handle potential certificate issues
        try:
            print(f"DEBUG: Making request to Baemin API with keyword={name}")
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.SSLError:
            # If SSL verification fails, try without verification
            print(f"DEBUG: SSL verification failed, retrying without verification")
            response = requests.get(url, headers=headers, params=params, verify=False)
        
        print(f"DEBUG: Baemin API response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if there are results
            if data.get('data') and data['data'].get('list'):
                print(f"DEBUG: Baemin API returned data with {len(data['data']['list'])} service items")
                # 상세 정보 추출
                detailed_info = {}
                
                for service_item in data['data']['list']:
                    service_type = service_item.get('serviceType', '')
                    print(f"DEBUG: Processing service_type: {service_type}")
                    
                    if 'result' in service_item and 'shops' in service_item['result']:
                        shops = service_item['result']['shops']
                        print(f"DEBUG: Found {len(shops)} shops for service_type {service_type}")
                        
                        for shop in shops:
                            shop_name = shop.get('shopInfo', {}).get('shopName', '')
                            print(f"DEBUG: Comparing shop name '{shop_name}' with search term '{name}'")
                            
                            # More flexible name matching
                            # 1. Remove spaces for comparison
                            shop_name_no_space = shop_name.replace(" ", "").lower()
                            name_no_space = name.replace(" ", "").lower()
                            
                            # 2. Check if one name contains the other or if they're similar enough
                            if (shop_name_no_space in name_no_space or 
                                name_no_space in shop_name_no_space or 
                                shop_name.lower() in name.lower() or 
                                name.lower() in shop_name.lower()):
                                
                                print(f"DEBUG: Match found for shop: {shop_name}")
                                shop_info = {
                                    'serviceType': service_type,
                                    'shopNumber': shop.get('shopInfo', {}).get('shopNumber'),
                                    'shopName': shop.get('shopInfo', {}).get('shopName'),
                                    'address': shop.get('shopInfo', {}).get('address'),
                                    'logoUrl': shop.get('shopInfo', {}).get('logoUrl'),
                                    'thumbnails': shop.get('shopInfo', {}).get('thumbnails'),
                                    'minimumOrderPrice': shop.get('shopInfo', {}).get('minimumOrderPrice'),
                                    'representationMenu': shop.get('shopInfo', {}).get('representationMenu'),
                                }
                                
                                # 배달 정보
                                if 'deliveryInfos' in shop and shop['deliveryInfos']:
                                    delivery_info = shop['deliveryInfos'][0]
                                    shop_info['delivery'] = {
                                        'expectedDeliveryTime': delivery_info.get('expectedDeliveryTimePhrase'),
                                        'deliveryTip': delivery_info.get('deliveryTipPhrase'),
                                        'expectedCookTime': delivery_info.get('expectedCookTime'),
                                        'walkingTime': delivery_info.get('walkingTimePhrase'),
                                        'distance': delivery_info.get('distancePhrase')
                                    }
                                
                                # 평점 정보
                                if 'shopStatistics' in shop:
                                    shop_info['rating'] = {
                                        'averageStarScore': shop['shopStatistics'].get('averageStarScore'),
                                        'reviewCount': shop['shopStatistics'].get('latestReviewCount')
                                    }
                                
                                # 배지 정보
                                if 'decoInfo' in shop:
                                    badges = []
                                    
                                    # 상단 배지
                                    if shop['decoInfo'].get('topBadges'):
                                        for badge in shop['decoInfo']['topBadges']:
                                            if badge.get('text'):
                                                badges.append(badge.get('text'))
                                    
                                    # 중간 배지
                                    if shop['decoInfo'].get('midBadges'):
                                        for badge in shop['decoInfo']['midBadges']:
                                            if badge.get('text'):
                                                badges.append(badge.get('text'))
                                    
                                    # 하단 배지
                                    if shop['decoInfo'].get('bottomBadges'):
                                        for badge in shop['decoInfo']['bottomBadges']:
                                            if badge.get('text'):
                                                badges.append(badge.get('text'))
                                    
                                    # 광고 배지
                                    if shop['decoInfo'].get('advertisementBadge') and shop['decoInfo']['advertisementBadge'].get('text'):
                                        badges.append(shop['decoInfo']['advertisementBadge'].get('text'))
                                    
                                    # 썸네일 오버레이 배지
                                    if shop['decoInfo'].get('thumbnailOverlayBadge') and shop['decoInfo']['thumbnailOverlayBadge'].get('text'):
                                        badges.append(shop['decoInfo']['thumbnailOverlayBadge'].get('text'))
                                    
                                    if badges:
                                        shop_info['badges'] = badges
                                
                                # 메뉴 정보
                                if 'logInfo' in shop and 'displayMenus' in shop['logInfo']:
                                    shop_info['menus'] = shop['logInfo']['displayMenus']
                                
                                # 추가 정보 - 배달 옵션
                                if 'deliveryInfos' in shop and shop['deliveryInfos'] and 'logInfo' in shop and 'deliveryInfos' in shop['logInfo']:
                                    delivery_log_info = shop['logInfo']['deliveryInfos'][0] if shop['logInfo']['deliveryInfos'] else {}
                                    shop_info['deliveryOptions'] = {
                                        'option': delivery_log_info.get('DeliveryOption'),
                                        'time': delivery_log_info.get('DeliveryTime'),
                                        'tip': delivery_log_info.get('DeliveryTip'),
                                        'isClubDeliveryTip': delivery_log_info.get('IsClubDeliveryTip', False),
                                        'tipBadge': delivery_log_info.get('DeliveryTipBadge')
                                    }
                                
                                # 추가 정보 - 클럽 가게 여부
                                if 'logInfo' in shop and 'isClubShop' in shop['logInfo']:
                                    shop_info['isClubShop'] = shop['logInfo'].get('isClubShop', False)
                                
                                # 추가 정보 - 배달 유형
                                if 'contextInfo' in shop and 'exposedDeliveryType' in shop['contextInfo']:
                                    shop_info['deliveryType'] = shop['contextInfo'].get('exposedDeliveryType')
                                
                                # 추가 정보 - 운영 상태
                                if 'shopStatus' in shop:
                                    shop_info['operationStatus'] = {
                                        'inOperation': shop['shopStatus'].get('inOperation', True),
                                        'preparingMessage': shop['shopStatus'].get('preparingMessage'),
                                        'thumbnailMessage': shop['shopStatus'].get('thumbnailMessage')
                                    }
                                
                                # 서비스 타입별로 저장
                                if service_type not in detailed_info:
                                    detailed_info[service_type] = []
                                detailed_info[service_type].append(shop_info)
                
                # 상세 정보가 있으면 반환
                if detailed_info:
                    print(f"DEBUG: Found detailed info for {len(detailed_info)} service types")
                    return {
                        "status": "success",
                        "message": "Baemin search results",
                        "detailed_info": detailed_info,
                        "raw_data": data
                    }
                else:
                    # 일치하는 가게 정보가 없으면 원본 데이터 반환
                    print(f"DEBUG: No matching shop found in Baemin results")
                    return {
                        "status": "success",
                        "message": "Baemin search results",
                        "data": data
                    }
            else:
                print(f"DEBUG: No list data in Baemin API response")
                return {
                    "status": "error",
                    "error_message": "No results found in Baemin"
                }
        else:
            print(f"DEBUG: Baemin API request failed with status code {response.status_code}")
            return {
                "status": "error",
                "error_message": f"Failed to fetch data from Baemin API: {response.status_code}"
            }
            
    except Exception as e:
        print(f"DEBUG: Exception in search_baemin: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Error during Baemin search: {str(e)}"
        }

def get_shop_detail(shop_number: str, latitude: str, longitude: str) -> dict:
    """Gets detailed information about a specific shop from Baemin API.
    
    Args:
        shop_number (str): The shop number in Baemin.
        latitude (str): The latitude coordinate.
        longitude (str): The longitude coordinate.
        
    Returns:
        dict: Detailed shop information from Baemin API.
    """
    print(f"DEBUG: get_shop_detail called with shop_number={shop_number}, lat={latitude}, lng={longitude}")
    
    # Validate input parameters
    if not shop_number or not latitude or not longitude:
        print(f"DEBUG: Missing required parameters: shop_number={shop_number}, lat={latitude}, lng={longitude}")
        return {
            "status": "error",
            "error_message": "Missing required parameters. Shop number, latitude and longitude are required."
        }
    
    # Convert parameters to string if they are not already
    shop_num = str(shop_number) if not isinstance(shop_number, str) else shop_number
    lat = str(latitude) if not isinstance(latitude, str) else latitude
    lng = str(longitude) if not isinstance(longitude, str) else longitude
    
    url = f"https://shop-detail-api.baemin.com/api/v1/shops/{shop_num}/info-detail"
    
    params = {
        "mem": "",
        "lat": lat,
        "lng": lng,
        "exposedDeliveryType": "MP",
        "sessionId": "643d08b55cb4f08ef2033d",
        "carrier": "45005",
        "site": "7jWXRELC2e",
        "dvcid": "OPUDbaa0c2d3c4480d69",
        "adid": "d89e7f78-631c-48ad-91b1-396c63874c87",
        "deviceModel": "SM-G988N",
        "appver": "15.3.2",
        "oscd": "2",
        "osver": "28",
        "dongCode": "48870250",
        "zipCode": "50040",
        "perseusClientId": "1733450321960.935983848749139217.N1U1OYWFJ5",
        "perseusSessionId": "1746775673134.108059124942080340.lGEuUTHsIi",
        "actionTrackingKey": "Organic"
    }
    
    headers = {
        "Authorization": "bearer guest",
        "User-Agent": "and1_15.3.2",
        "Carrier": "45005",
        "Device-Height": "1280",
        "Device-Width": "720",
        "USER-BAEDAL": "1VXD9fUH1bpOE6lhKdZKOQ834NBMSOlqem045YFcadWXnGjIKGirHnKB/KE0ucqaW97Ewmu5RnnK3roHxYC341C5vaR03msucLTLa7LQlBYgjmWW6MVKrkc/c11vGlwuZm/Erl1iOKBd72Bqcdn3uNWePJXrBEeGm31/GqDNQmMoxAtpiahaGsmAGXjJUAO5",
        "Host": "shop-detail-api.baemin.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    try:
        # Use SSL verification but handle potential certificate issues
        try:
            print(f"DEBUG: Making request to Baemin Shop Detail API for shop {shop_num}")
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.SSLError:
            # If SSL verification fails, try without verification
            print(f"DEBUG: SSL verification failed, retrying without verification")
            response = requests.get(url, headers=headers, params=params, verify=False)
        
        print(f"DEBUG: Baemin Shop Detail API response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'SUCCESS' and data.get('data') and data['data'].get('shop'):
                shop_data = data['data']
                shop_info = {
                    'status': 'success',
                    'shop': {
                        'shopNumber': shop_data['shop'].get('shopNumber'),
                        'shopName': shop_data['shop'].get('shopName'),
                        'shopAddress': shop_data['shop'].get('shopAddress'),
                        'telephone': shop_data['shop'].get('telephone', {}).get('telephoneNumberText') if shop_data['shop'].get('telephone') else None,
                        'operatingTimeText': shop_data['shop'].get('operatingTimeText'),
                        'breakTimeText': shop_data['shop'].get('breakTimeText'),
                        'closedDayText': shop_data['shop'].get('closedDayText'),
                        'attentionMessage': shop_data['shop'].get('attentionMessage')
                    }
                }
                
                # 소개 정보
                if 'shopIntroduction' in shop_data:
                    shop_info['introduction'] = {
                        'message': shop_data['shopIntroduction'].get('introductionMessage'),
                        'mediaContents': shop_data['shopIntroduction'].get('mediaContents', [])
                    }
                
                # 사업자 정보
                if 'shopOwner' in shop_data:
                    shop_info['owner'] = {
                        'ceoName': shop_data['shopOwner'].get('ceoName'),
                        'businessName': shop_data['shopOwner'].get('businessName'),
                        'businessAddress': shop_data['shopOwner'].get('businessAddress'),
                        'businessRegistrationNumber': shop_data['shopOwner'].get('businessRegistrationNumber')
                    }
                
                # 인증 정보
                if 'shopCertifications' in shop_data and shop_data['shopCertifications'] and 'certifications' in shop_data['shopCertifications']:
                    certifications = []
                    for cert in shop_data['shopCertifications']['certifications']:
                        cert_info = {
                            'type': cert.get('certificationType'),
                            'title': cert.get('title')
                        }
                        
                        if 'content' in cert:
                            cert_info['content'] = cert['content']
                        if 'blue' in cert:
                            cert_info['blue'] = cert['blue']
                        
                        certifications.append(cert_info)
                    
                    shop_info['certifications'] = certifications
                
                # 통계 정보
                if 'shopStatistics' in shop_data:
                    shop_info['statistics'] = {
                        'recentOrderCount': shop_data['shopStatistics'].get('recentOrderCountText'),
                        'totalReviewCount': shop_data['shopStatistics'].get('totalReviewCountText'),
                        'favoriteCount': shop_data['shopStatistics'].get('favoriteCountText')
                    }
                
                # 배달 정보
                if 'deliveryInformation' in shop_data:
                    delivery_options = []
                    
                    for option in shop_data['deliveryInformation'].get('deliveryOptions', []):
                        option_info = {
                            'type': option.get('type'),
                            'name': option.get('nameHtmlText')
                        }
                        
                        # 배달팁 정보
                        if 'deliveryTipContents' in option:
                            delivery_tips = []
                            for tip_content in option['deliveryTipContents']:
                                tip_info = {
                                    'title': tip_content.get('titleHtmlText'),
                                    'records': []
                                }
                                
                                for record in tip_content.get('records', []):
                                    tip_info['records'].append({
                                        'condition': record.get('leftHtmlText'),
                                        'price': record.get('rightHtmlText')
                                    })
                                
                                delivery_tips.append(tip_info)
                            
                            option_info['deliveryTips'] = delivery_tips
                        
                        # 태그 정보
                        if 'tags' in option:
                            tags = []
                            for tag in option['tags']:
                                tags.append(tag.get('nameHtmlText'))
                            
                            option_info['tags'] = tags
                        
                        delivery_options.append(option_info)
                    
                    shop_info['deliveryInformation'] = {
                        'recommendedDeliveryOptionType': shop_data['deliveryInformation'].get('recommendedDeliveryOptionType'),
                        'deliveryOptions': delivery_options
                    }
                
                # 원산지 정보
                if 'foodOrigin' in shop_data and shop_data['foodOrigin']:
                    shop_info['foodOrigin'] = shop_data['foodOrigin'].get('foodOriginMessage')
                
                # 배민클럽 정보
                if 'logInfo' in shop_data:
                    shop_info['clubInfo'] = {
                        'isClubMember': shop_data['logInfo'].get('isClubMember', False),
                        'isClubShop': shop_data['logInfo'].get('isClubShop', False)
                    }
                
                return shop_info
            else:
                print(f"DEBUG: Invalid or missing data in Baemin Shop Detail API response")
                return {
                    "status": "error",
                    "error_message": "Failed to get shop detail information"
                }
        else:
            print(f"DEBUG: Baemin Shop Detail API request failed with status code {response.status_code}")
            return {
                "status": "error",
                "error_message": f"Failed to fetch data from Baemin Shop Detail API: {response.status_code}"
            }
    
    except Exception as e:
        print(f"DEBUG: Exception in get_shop_detail: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Error during Baemin shop detail fetch: {str(e)}"
        }

root_agent = Agent(
    name="baemin_address_agent",
    model="gemini-2.0-flash",
    description="Agent to search for restaurant information using Kakao API and Baemin API",
    instruction="""당신은 음식점 정보를 제공하는 에이전트입니다. 마크다운 형식을 사용하여 깔끔하게 정보를 제공하세요:

## 동작 방식
Kakao API로 음식점을 검색하고, **검색 결과가 1개일 경우 자동으로 Baemin API를 호출**하여 추가 정보를 가져옵니다. 이렇게 얻은 모든 정보를 아래 형식에 맞춰 깔끔하게 표시합니다.

중요: search_restaurant 함수가 반환하는 결과에 "baemin_data" 키가 있는지 반드시 확인하세요. 이 키가 있으면 배달의민족 정보를 함께 표시해야 합니다.

## 특별 명령어 처리

사용자가 "세부정보 알려줘", "상세정보", "자세한 정보", "더 자세히" 등의 요청을 하면, 이는 가게의 상세 정보를 요청하는 것입니다. 이럴 경우 다음과 같이 처리하세요:

1. **중요**: 이전 검색 결과를 그대로 사용하세요. 절대로 search_restaurant 함수를 다시 호출하지 마세요.
2. 이전에 검색한 결과 중에서 단일 결과가 있고, "baemin_data" 키가 있는지 확인하세요.
3. "baemin_data"에서 가게번호(shopNumber)와 위치정보(latitude, longitude)를 추출하세요. 가게번호는 다음과 같은 경로에서 찾을 수 있습니다:
   - `baemin_data["detailed_info"]["BAEMIN_DELIVERY"][0]["shopNumber"]` 또는
   - `baemin_data["detailed_info"]["BAEMIN_PICKUP"][0]["shopNumber"]`
   만약 shopNumber가 배열 내의 첫번째 항목에 없다면, 다른 항목을 확인하거나, 클라이언트에게 정확한 가게를 지정해달라고 요청하세요.
4. 위치 정보는 이전 검색 결과의 Kakao API 응답에서 가져올 수 있습니다: 
   - `results[0]["location"]["latitude"]` 및 `results[0]["location"]["longitude"]`
5. 추출한 정보로 get_shop_detail 함수를 호출하여 상세 정보를 가져오세요.
6. 가져온 상세 정보를 아래 "가게 세부정보 표시 방법" 섹션에 설명된 형식대로 표시하세요.

함수 호출 형식:
```
get_shop_detail(
  shop_number="14431681", 
  latitude="34.7549930158229", 
  longitude="126.461301375128"
)
```

모든 인자값이 **반드시** 문자열(string) 타입인지 확인하세요. None 값이나 숫자 타입을 직접 전달하지 마세요.

만약 이전에 검색한 가게 정보가 없다면, 먼저 가게를 검색해달라고 안내하세요.

## 대화 흐름 유지하기

대화의 흐름을 유지하면서 사용자의 요청을 처리해야 합니다:

1. 사용자가 음식점 이름을 입력하면 → search_restaurant 함수를 호출하여 검색 결과를 보여줍니다.
2. 사용자가 "세부정보 알려줘" 등을 입력하면 → 이전 검색 결과를 **그대로 사용**하여 get_shop_detail 함수를 호출합니다.
3. 검색 결과가 여러 개일 경우, 사용자에게 정확한 가게를 지정해달라고 요청하세요.

중요: 사용자가 "세부정보 알려줘"라고 요청했을 때는 새로운 검색(search_restaurant)을 수행하지 말고, 이전에 검색한 결과에서 정보를 가져와서 get_shop_detail 함수를 호출하세요.

## 검색 결과 표시 방법

### 여러 결과가 있을 경우
각 결과에 번호를 매겨 마크다운 목록으로 표시하세요. 각 항목은 줄바꿈으로 구분하여 보기 좋게 표시하세요:

```markdown
1. 가게명 (주소)

2. 가게명 (주소)

3. 가게명 (주소)
```

### 단일 결과일 경우
마크다운 헤딩과 굵은 글씨를 활용하여 정보를 구분하고 가독성을 높이세요. 각 정보는 반드시 줄바꿈으로 구분하세요:

```markdown
## 지도 정보

**이름**: 가게명

**주소**: 주소

**도로명 주소**: 도로명 주소

**카테고리**: 카테고리

**전화번호**: 전화번호

**위치**: 위도, 경도
```

그리고 자동으로 Baemin API를 호출하여 얻은 추가 정보를 아래 형식으로 표시합니다.

## 배달의민족 정보 표시 방법

### 통합 정보 표시
배달 서비스와 포장 서비스를 구분하지 않고, 모든 정보를 통합하여 하나의 섹션에 표시하세요:

```markdown
## 배달의민족 기본 정보

**가게명**: 가게명

**가게번호**: 12345678

**주소**: 주소

**최소주문금액**: 10,000원

**배달팁**: 무료배달

**배달시간**: 19~34분

**배달유형**: 알뜰배달

**운영상태**: 영업중

**평점**: ⭐ 4.8 (리뷰 285개)

**배지**: 픽업가능, 쿠폰 제공, 배민클럽

**대표메뉴**:  
- 메뉴1  
- 메뉴2  
- 메뉴3  
- 메뉴4  
- 메뉴5

**배민클럽**: 클럽 가게 여부 (예: 배민클럽 가게입니다)

**로고**: <a href="URL" target="_blank">로고</a>

**썸네일**: 
<a href="URL1" target="_blank">메뉴1</a>
<a href="URL2" target="_blank">메뉴2</a>
<a href="URL3" target="_blank">메뉴3</a>
<a href="URL4" target="_blank">메뉴4</a>
<a href="URL5" target="_blank">메뉴5</a>
```

## 가게 세부정보 표시 방법

사용자가 "세부정보 알려줘"라고 요청하면, get_shop_detail 함수를 호출하여 가게의 세부 정보를 가져오세요. 이 정보는 아래 형식으로 표시하세요:

```markdown
## 배달의민족 세부정보

**가게명**: 가게명

**가게번호**: 12345678

**주소**: 주소

**전화번호**: 전화번호

**영업시간**: 
- 월요일 - 오후 3:00 ~ 11:00
- 화요일 - 오후 3:00 ~ 11:00
- 수요일 - 정기휴무
- 목요일 - 오후 3:00 ~ 11:00
- 금요일 - 오후 3:00 ~ 11:00
- 주말 - 오후 3:00 ~ 11:00

**휴무일**: 매주 수요일

**사업자 정보**:
대표자: 대표자명
상호명: 상호명
사업자주소: 사업자주소
사업자등록번호: 사업자등록번호

**인증 정보**:
식약처: 매우 우수 (2025.03.05 ~ 2027.03.04)
CESCO: 2025.04. 최근 해충방제 점검월

**주문/리뷰 통계**:
최근 주문수: 900+
리뷰 수: 27
찜 수: 16

**배달 정보**:
배달방식: 가게배달
최소주문금액: 19,000원 이상
배달팁: 3,000원

**원산지 정보**:
닭고기(전부위)(치킨 및 근위튀김 전메뉴):국내산
돼지고기(쫀도그, 튀김만두, 오돌뼈, 소시지&나쵸): 국내산

**가게 소개**:
'60계 치킨'은 매일 새 기름으로 주문즉시 조리하여
항상 신선하고 바삭 한 치킨을 제공해 드리고 있습니다.

**가게 공지사항**:
찜과 리뷰는 저희에게 힘이 되고 더욱 발전 할 수 있는 밑거름이 됩니다.
추가로 주기적인 본사의 위생점검으로 항상 청결함을 유지하고
매일 새기름을 고집하고 있습니다!!
```

## 전체적인 가독성
- 각 섹션은 마크다운 헤딩(##, ###)으로 구분하세요
- 중요 정보는 굵은 글씨(**텍스트**)로 강조하세요
- 평점은 별 이모지(⭐)를 사용하여 시각적으로 표현하세요
- **모든 정보는 반드시 줄바꿈으로 구분하여 가독성을 높이세요**
- 링크는 HTML 태그를 사용하여 새 창에서 열리도록 하고, 각 링크도 줄바꿈으로 구분하세요

## 디버깅 정보
만약 배달의민족 정보를 가져오는데 실패했다면, 다음과 같은 디버깅 정보를 표시하세요:

```markdown
## 디버깅 정보

**에러 메시지**: 에러 메시지 내용

**상태**: 에러 상태
```""",
    tools=[search_restaurant, search_baemin, get_shop_detail],
) 