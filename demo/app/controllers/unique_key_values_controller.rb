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

  def update_key
    @kvp = UniqueKeyValue.find_by(key: uniquekeyvalue_params[:key])
    if @kvp
      @kvp.update!(uniquekeyvalue_params)
      render plain: "Success!"
    else
      render plain: "ERROR: nil"
    end
  end

  def get_key
    @kvp = UniqueKeyValue.find_by(key: uniquekeyvalue_params[:key])
    if @kvp
      render json: @kvp
    else
      render plain: "ERROR: nil"
    end
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

  def destroy_key
    @nrec  = UniqueKeyValue.destroy_all(key: uniquekeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
  end

  def delete_key
    @nrec  = UniqueKeyValue.delete_all(key: uniquekeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
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
