"""
公众号管理API端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app.core.database import get_db
from app.models.wechat_account import WechatAccount
from app.schemas.wechat_account import (
    WechatAccountCreate, 
    WechatAccountUpdate, 
    WechatAccountResponse,
    WechatAccountList
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=WechatAccountList)
async def get_wechat_accounts(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    nickname: Optional[str] = Query(None, description="公众号名称"),
    biz: Optional[str] = Query(None, description="公众号biz"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: Session = Depends(get_db)
):
    """获取公众号列表"""
    try:
        query = db.query(WechatAccount)
        
        # 添加过滤条件
        if nickname:
            query = query.filter(WechatAccount.nickname.ilike(f"%{nickname}%"))
        if biz:
            query = query.filter(WechatAccount.biz == biz)
        if is_active is not None:
            query = query.filter(WechatAccount.is_active == is_active)
        
        # 获取总数
        total = query.count()
        
        # 分页
        accounts = query.offset(skip).limit(limit).all()
        
        return WechatAccountList(
            accounts=[WechatAccountResponse.from_orm(account) for account in accounts],
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"获取公众号列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取公众号列表失败")


@router.get("/{account_id}", response_model=WechatAccountResponse)
async def get_wechat_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """获取单个公众号信息"""
    try:
        account = db.query(WechatAccount).filter(WechatAccount.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="公众号不存在")
        
        return WechatAccountResponse.from_orm(account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取公众号信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取公众号信息失败")


@router.get("/by-nickname/{nickname}", response_model=WechatAccountResponse)
async def get_wechat_account_by_nickname(
    nickname: str,
    db: Session = Depends(get_db)
):
    """根据公众号名称获取信息"""
    try:
        account = db.query(WechatAccount).filter(
            WechatAccount.nickname == nickname
        ).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="公众号不存在")
        
        return WechatAccountResponse.from_orm(account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"根据名称获取公众号信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取公众号信息失败")


@router.get("/by-biz/{biz}", response_model=WechatAccountResponse)
async def get_wechat_account_by_biz(
    biz: str,
    db: Session = Depends(get_db)
):
    """根据公众号biz获取信息"""
    try:
        account = db.query(WechatAccount).filter(WechatAccount.biz == biz).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="公众号不存在")
        
        return WechatAccountResponse.from_orm(account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"根据biz获取公众号信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取公众号信息失败")


@router.post("/", response_model=WechatAccountResponse)
async def create_wechat_account(
    account: WechatAccountCreate,
    db: Session = Depends(get_db)
):
    """创建公众号"""
    try:
        # 检查是否已存在
        existing = db.query(WechatAccount).filter(
            or_(
                WechatAccount.biz == account.biz,
                WechatAccount.nickname == account.nickname
            )
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="公众号已存在")
        
        # 创建新公众号
        db_account = WechatAccount(**account.dict())
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        
        return WechatAccountResponse.from_orm(db_account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建公众号失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="创建公众号失败")


@router.put("/{account_id}", response_model=WechatAccountResponse)
async def update_wechat_account(
    account_id: int,
    account_update: WechatAccountUpdate,
    db: Session = Depends(get_db)
):
    """更新公众号信息"""
    try:
        db_account = db.query(WechatAccount).filter(WechatAccount.id == account_id).first()
        if not db_account:
            raise HTTPException(status_code=404, detail="公众号不存在")
        
        # 更新字段
        update_data = account_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_account, field, value)
        
        db.commit()
        db.refresh(db_account)
        
        return WechatAccountResponse.from_orm(db_account)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新公众号失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新公众号失败")


@router.delete("/{account_id}")
async def delete_wechat_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """删除公众号"""
    try:
        db_account = db.query(WechatAccount).filter(WechatAccount.id == account_id).first()
        if not db_account:
            raise HTTPException(status_code=404, detail="公众号不存在")
        
        db.delete(db_account)
        db.commit()
        
        return {"message": "公众号删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除公众号失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="删除公众号失败")


@router.get("/stats/overview")
async def get_accounts_stats(db: Session = Depends(get_db)):
    """获取公众号统计概览"""
    try:
        total_accounts = db.query(WechatAccount).count()
        active_accounts = db.query(WechatAccount).filter(WechatAccount.is_active == True).count()
        verified_accounts = db.query(WechatAccount).filter(WechatAccount.is_verified == True).count()
        
        # 获取文章总数
        total_articles = db.query(WechatAccount.article_count).scalar() or 0
        
        return {
            "total_accounts": total_accounts,
            "active_accounts": active_accounts,
            "verified_accounts": verified_accounts,
            "total_articles": total_articles
        }
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取统计信息失败") 