class CreateBelongsToUsers < ActiveRecord::Migration
  def change
    create_table :belongs_to_users do |t|
      t.belongs_to :belongs_to_department, index: true

      t.timestamps
    end
  end
end
