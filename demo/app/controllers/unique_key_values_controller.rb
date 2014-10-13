class UniqueKeyValuesController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @kvp = UniqueKeyValue.new(uniquekeyvalue_params)
      @kvp.save!
      puts @kvp.id
      render json: @kvp

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def update
    @kvp = UniqueKeyValue.find(params[:key])
    @kvp.update(uniquekeyvalue_params)
  end

  def index
    render json: UniqueKeyValue.all()
  end

  def destroy
    begin
      UniqueKeyValue.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

  def destroy_all
    begin
      UniqueKeyValue.find_by_key(params[:key]) do |r| 
        r.destroy_all
      end
    end
  end


private
  def uniquekeyvalue_params
    params.require(:unique_key_value).permit(:key, :value, :id)
  end
end
