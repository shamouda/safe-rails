class BelongsToUser < ActiveRecord::Base
  belongs_to :belongs_to_department, :dependent => :delete
  validates :belongs_to_department, :presence => true
end
