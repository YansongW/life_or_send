"""initial

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wx_open_id', sa.String(64), unique=True, index=True),
        sa.Column('nickname', sa.String(64), nullable=True),
        sa.Column('role', sa.Enum('USER', 'ADMIN', name='userrole'), default='USER'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('last_active_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建会话表
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(64), index=True),
        sa.Column('session_id', sa.String(64), unique=True, index=True),
        sa.Column('title', sa.String(255)),
        sa.Column('context', sa.Text),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建消息表
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(64), index=True),
        sa.Column('session_id', sa.String(64), index=True),
        sa.Column('content', sa.Text),
        sa.Column('message_type', sa.String(20)),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('vector_id', sa.String(64), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.session_id'])
    )

def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('chat_sessions')
    op.drop_table('users') 