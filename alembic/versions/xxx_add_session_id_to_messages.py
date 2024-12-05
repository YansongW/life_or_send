"""add session id to messages

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 添加session_id列
    op.add_column('messages', sa.Column('session_id', sa.String(64), nullable=True))
    
    # 创建外键
    op.create_foreign_key(
        'fk_message_session',
        'messages',
        'chat_sessions',
        ['session_id'],
        ['session_id']
    )
    
    # 创建索引
    op.create_index(
        'ix_messages_session_id',
        'messages',
        ['session_id']
    )

def downgrade():
    # 删除外键
    op.drop_constraint('fk_message_session', 'messages', type_='foreignkey')
    
    # 删除索引
    op.drop_index('ix_messages_session_id', 'messages')
    
    # 删除列
    op.drop_column('messages', 'session_id') 