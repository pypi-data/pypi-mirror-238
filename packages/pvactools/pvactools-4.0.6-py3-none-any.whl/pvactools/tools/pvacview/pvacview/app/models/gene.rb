class Gene < ApplicationRecord
  has_many :transcripts

  validates :ensembl_id, presence: true
end
