class User < ActiveRecord::Base
  validates :name, presence: true, uniqueness: true
  validates :age, presence: true
end
