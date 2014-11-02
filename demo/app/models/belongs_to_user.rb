class BelongsToUser < ActiveRecord::Base
  belongs_to :belongs_to_department
  validates :belongs_to_department, :presence => true
end
