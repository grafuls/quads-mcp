"""
QUADS MCP tools implementation.
This file contains tool implementations for the QUADS API operations.
"""

from .. import server
from ..server import mcp, Context
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime


@mcp.tool()
async def quads_login(username: str, password: str, ctx: Context) -> Dict[str, Any]:
    """
    Login to QUADS API and get authentication token.
    
    Args:
        username: Username for authentication
        password: Password for authentication
        ctx: The Context object (automatically injected)
        
    Returns:
        Authentication token and status
    """
    import httpx
    
    try:
        # Get the QUADS API base URL from config
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info(f"Logging in to QUADS API at {base_url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/login/",
                auth=(username, password),
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            ctx.info("Successfully logged in to QUADS")
            return result
            
    except httpx.HTTPStatusError as e:
        error_msg = f"Login failed: HTTP {e.response.status_code}"
        ctx.error(error_msg)
        return {"error": error_msg, "status_code": e.response.status_code}
    except Exception as e:
        error_msg = f"Login error: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_clouds(ctx: Context) -> Dict[str, Any]:
    """
    Get all defined clouds from QUADS.
    
    Args:
        ctx: The Context object (automatically injected)
        
    Returns:
        List of all clouds
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info("Fetching all clouds from QUADS")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/clouds/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} clouds")
            return {"clouds": result}
            
    except Exception as e:
        error_msg = f"Failed to get clouds: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_free_clouds(ctx: Context) -> Dict[str, Any]:
    """
    Get all free clouds available for new assignments.
    
    Args:
        ctx: The Context object (automatically injected)
        
    Returns:
        List of free clouds
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info("Fetching free clouds from QUADS")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/clouds/free/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} free clouds")
            return {"free_clouds": result}
            
    except Exception as e:
        error_msg = f"Failed to get free clouds: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_hosts(name: Optional[str] = None, model: Optional[str] = None, 
                         host_type: Optional[str] = None, broken: Optional[bool] = None,
                         ctx: Context = None) -> Dict[str, Any]:
    """
    Get hosts from QUADS with optional filtering.
    
    Args:
        name: Filter hosts by name
        model: Filter hosts by model name
        host_type: Filter hosts by type
        broken: Filter by broken status
        ctx: The Context object (automatically injected)
        
    Returns:
        List of hosts matching the criteria
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        # Build query parameters
        params = {}
        if name:
            params['name'] = name
        if model:
            params['model'] = model
        if host_type:
            params['host_type'] = host_type
        if broken is not None:
            params['broken'] = str(broken).lower()
        
        ctx.info(f"Fetching hosts from QUADS with filters: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/hosts/", params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} hosts")
            return {"hosts": result, "filters": params}
            
    except Exception as e:
        error_msg = f"Failed to get hosts: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_host_details(hostname: str, ctx: Context) -> Dict[str, Any]:
    """
    Get detailed information about a specific host.
    
    Args:
        hostname: The hostname to get details for
        ctx: The Context object (automatically injected)
        
    Returns:
        Detailed host information including hardware specs
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info(f"Fetching details for host: {hostname}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/hosts/{hostname}/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved details for host {hostname}")
            return {"host": result}
            
    except Exception as e:
        error_msg = f"Failed to get host details for {hostname}: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_available_hosts(start: Optional[str] = None, end: Optional[str] = None,
                                   cloud: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Get available hosts for a specific time period.
    
    Args:
        start: Start date (YYYY-MM-DD format)
        end: End date (YYYY-MM-DD format)
        cloud: Filter by cloud name
        ctx: The Context object (automatically injected)
        
    Returns:
        List of available hosts
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        params = {}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if cloud:
            params['cloud'] = cloud
        
        ctx.info(f"Fetching available hosts with parameters: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/available/", params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} available hosts")
            return {"available_hosts": result, "parameters": params}
            
    except Exception as e:
        error_msg = f"Failed to get available hosts: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_check_host_availability(hostname: str, start: Optional[str] = None, 
                                       end: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Check if a specific host is available for a given time period.
    
    Args:
        hostname: The hostname to check
        start: Start date (YYYY-MM-DD format)
        end: End date (YYYY-MM-DD format)
        ctx: The Context object (automatically injected)
        
    Returns:
        Host availability status
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        params = {}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        
        ctx.info(f"Checking availability for host {hostname} with parameters: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/available/{hostname}/", params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Checked availability for host {hostname}")
            return {"hostname": hostname, "availability": result, "parameters": params}
            
    except Exception as e:
        error_msg = f"Failed to check host availability for {hostname}: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_schedules(ctx: Context) -> Dict[str, Any]:
    """
    Get all defined schedules from QUADS.
    
    Args:
        ctx: The Context object (automatically injected)
        
    Returns:
        List of all schedules
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info("Fetching all schedules from QUADS")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/schedules/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} schedules")
            return {"schedules": result}
            
    except Exception as e:
        error_msg = f"Failed to get schedules: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_current_schedules(date: Optional[str] = None, host: Optional[str] = None,
                                     cloud: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Get current schedules with optional filtering.
    
    Args:
        date: Date to check current schedules for
        host: Filter by hostname
        cloud: Filter by cloud name
        ctx: The Context object (automatically injected)
        
    Returns:
        List of current schedules
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        params = {}
        if date:
            params['date'] = date
        if host:
            params['host'] = host
        if cloud:
            params['cloud'] = cloud
        
        ctx.info(f"Fetching current schedules with parameters: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/schedules/current/", params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved current schedules")
            return {"current_schedules": result, "parameters": params}
            
    except Exception as e:
        error_msg = f"Failed to get current schedules: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_assignments(ctx: Context) -> Dict[str, Any]:
    """
    Get all assignments from QUADS.
    
    Args:
        ctx: The Context object (automatically injected)
        
    Returns:
        List of all assignments
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info("Fetching all assignments from QUADS")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/assignments/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved assignments")
            return {"assignments": result}
            
    except Exception as e:
        error_msg = f"Failed to get assignments: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_active_assignments(cloud_name: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Get active assignments, optionally filtered by cloud.
    
    Args:
        cloud_name: Filter by specific cloud name
        ctx: The Context object (automatically injected)
        
    Returns:
        List of active assignments
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        if cloud_name:
            url = f"{base_url}/assignments/active/{cloud_name}/"
            ctx.info(f"Fetching active assignments for cloud: {cloud_name}")
        else:
            url = f"{base_url}/assignments/active/"
            ctx.info("Fetching all active assignments")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved active assignments")
            return {"active_assignments": result, "cloud_filter": cloud_name}
            
    except Exception as e:
        error_msg = f"Failed to get active assignments: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_moves(date: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
    """
    Get host moves/transitions for a specific date.
    
    Args:
        date: Date to get moves for (YYYY-MM-DD format)
        ctx: The Context object (automatically injected)
        
    Returns:
        List of host moves
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        params = {}
        if date:
            params['date'] = date
        
        ctx.info(f"Fetching moves with parameters: {params}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/moves/", params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} moves")
            return {"moves": result, "parameters": params}
            
    except Exception as e:
        error_msg = f"Failed to get moves: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}


@mcp.tool()
async def quads_get_version(ctx: Context) -> Dict[str, Any]:
    """
    Get QUADS version information.
    
    Args:
        ctx: The Context object (automatically injected)
        
    Returns:
        QUADS version information
    """
    import httpx
    
    try:
        app_ctx = mcp.get_request_context().lifespan_context
        config = app_ctx.config
        base_url = config.get('quads', {}).get('base_url', 'https://quads.example.com/api/v3')
        
        ctx.info("Fetching QUADS version")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/version/", timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            ctx.info("Retrieved QUADS version")
            return {"version": result}
            
    except Exception as e:
        error_msg = f"Failed to get version: {str(e)}"
        ctx.error(error_msg)
        return {"error": error_msg}