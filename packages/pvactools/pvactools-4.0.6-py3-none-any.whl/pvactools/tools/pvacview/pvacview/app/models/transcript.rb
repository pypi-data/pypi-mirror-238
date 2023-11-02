class Transcript < ApplicationRecord
  belongs_to :gene

  validates :ensembl_id, presence: true
  validates :tsl, presence: true
  validates :length, presence: true
  validates :biotype, presence: true
  validates :gene_id, presence: true
end
