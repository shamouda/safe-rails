class CreateDbfkDepartments < ActiveRecord::Migration
  def change
    create_table :dbfk_departments do |t|

      t.timestamps
    end
  end
end
