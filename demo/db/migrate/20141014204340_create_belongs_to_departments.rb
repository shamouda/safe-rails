class CreateBelongsToDepartments < ActiveRecord::Migration
  def change
    create_table :belongs_to_departments do |t|

      t.timestamps
    end
  end
end
