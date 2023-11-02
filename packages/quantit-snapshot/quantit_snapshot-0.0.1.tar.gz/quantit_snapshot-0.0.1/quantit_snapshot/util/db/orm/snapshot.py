from functools import reduce

from sqlalchemy import Column, Integer, String, ForeignKey, exists
from sqlalchemy.ext.declarative import declarative_base

from util.db.alchemy import AlchemyUtils, DBSess

Base = declarative_base()


class Model(object):
    seq: int

    def _eq(self, other, identity):
        return reduce(
            lambda x, y: x & y,
            (getattr(self, i) == getattr(other, i) for i in identity)
        )

    @classmethod
    def all(cls, sess):
        return sess.query(cls).all()

    @staticmethod
    def _from_name(model, identity_struct, sm_name):
        sm_name = sm_name.split(".")
        sm_name.remove(model.TYPE)
        return model(
            **dict(
                zip(
                    identity_struct, sm_name
                )
            )
        )

    @classmethod
    def _query_by_name(cls, sess, identity_struct, model_name):
        return cls._query(sess, identity_struct, model_name).one()

    @staticmethod
    def query(sess, identity_name):
        model_type, model_name = Model.type_and_name(identity_name)
        return Model.of(model_type).query(sess, model_name)

    @classmethod
    def _query(cls, sess, identity_struct, model_name):
        constructed = cls._from_name(cls, identity_struct, model_name)
        return sess.query(cls).filter(
            reduce(
                lambda x, y: x & y,
                (getattr(cls, i) == getattr(constructed, i) for i in identity_struct)
            )
        )

    @staticmethod
    def exists(sess, identity_name) -> bool:
        model_type, model_name = Model.type_and_name(identity_name)
        return Model.of(model_type).exists(sess, model_name)

    @classmethod
    def _exists(cls, sess, identity_struct, model_name) -> bool:
        constructed = cls._from_name(cls, identity_struct, model_name)
        return sess.query(
            exists().where(
                reduce(
                    lambda x, y: x & y,
                    (getattr(cls, i) == getattr(constructed, i) for i in identity_struct)
                )
            )
        ).scalar()

    @staticmethod
    def query_by_name(sess, identity_name):
        model_type, model_name = Model.type_and_name(identity_name)
        return Model.of(model_type).query_by_name(sess, model_name)

    @classmethod
    def local_seq_to_name(cls, sess, l_seq):
        return str(sess.query(cls).filter(cls.seq == l_seq).one())

    @staticmethod
    def type_and_name(identity_name):
        return identity_name.split(".", 1)

    @staticmethod
    def global_seq_of(sess, identity_name):
        return Model.query_by_name(sess, identity_name).global_.global_seq

    @staticmethod
    def get_global_seqs(identity_names):
        with DBSess.of("model") as sess:
            return [Model.query_by_name(sess, x).global_.global_seq for x in identity_names]


class Snapshot(Base, Model):
    __tablename__ = 'snapshot'

    seq = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String(45))
    source = Column(String(45))
    category = Column(String(45))
    name = Column(String(45))

    NAME_STRUCT = ('service', 'source', 'category', 'name')
    TYPE = 'snapshot'

    def __repr__(self):
        return ".".join([self.TYPE, *[getattr(self, i) for i in self.NAME_STRUCT]])

    def __eq__(self, other):
        return super()._eq(other, self.NAME_STRUCT)

    @classmethod
    def from_name(cls, sm_name):
        return super()._from_name(cls, cls.NAME_STRUCT, sm_name)

    @classmethod
    def query(cls, sess, sm_name):
        return super()._query(sess, cls.NAME_STRUCT, sm_name)

    @classmethod
    def query_by_name(cls, sess, sm_name):
        return super()._query_by_name(sess, cls.NAME_STRUCT, sm_name)

    @classmethod
    def exists(cls, sess, sm_name):
        return super()._exists(sess, cls.NAME_STRUCT, sm_name)

    @classmethod
    def select(cls, sess, select, by, value):
        if isinstance(select, str):
            return set(
                [
                    getattr(i, select) for i in sess.query(Snapshot).filter(getattr(Snapshot, by) == value).all()
                ]
            )
        else:
            return set(
                [
                    getattr(getattr(i, select[0]), select[1]) for i in
                    sess.query(Snapshot).filter(getattr(Snapshot, by) == value).all()
                ]
            )

    @classmethod
    def is_exist(session, service, source, category, name):
        existing_snapshot = session.query(Snapshot).filter_by(
            service=service,
            source=source,
            category=category,
            name=name
        ).first()


class SnapshotMeta(Base):
    __tablename__ = "snapshot_meta"

    seq = Column(Integer, ForeignKey('snapshot.seq', ondelete="CASCADE"), primary_key=True)
    author = Column(String(45), nullable=True)
    generate_filename = Column(String(64), nullable=True)
    cache_type = Column(String(6))
    description = Column(String(256), nullable=True)


if __name__ == '__main__':
    engine = AlchemyUtils.load_engine("snapshot")
    Base.metadata.create_all(engine)
